import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# 환경변수 로드
load_dotenv()

SERVER = os.getenv("SQL_SERVER", "localhost")
PORT = os.getenv("SQL_PORT", "1433")
DB = os.getenv("SQL_DB_DW", "AdventureWorksDW2022")
AUTH = os.getenv("SQL_AUTH", "windows").lower()
USER = os.getenv("SQL_USERNAME")
PWD = os.getenv("SQL_PASSWORD")

# ODBC 연결 설정 (현재 환경은 Driver 17)
if AUTH == "windows":
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={SERVER},{PORT};Database={DB};"
        f"Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes;"
    )
else:
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={SERVER},{PORT};Database={DB};"
        f"Uid={USER};Pwd={PWD};Encrypt=yes;TrustServerCertificate=yes;"
    )

# SQL 쿼리
sql = """
SELECT
    d.CalendarYear AS [Year],
    d.MonthNumberOfYear AS [Month],
    SUM(f.SalesAmount) AS SalesAmount
FROM dbo.FactInternetSales AS f
JOIN dbo.DimDate AS d ON f.OrderDateKey = d.DateKey
GROUP BY d.CalendarYear, d.MonthNumberOfYear
ORDER BY [Year], [Month];
"""

# DB 연결 및 데이터 읽기
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(sql, conn)

# 시각화
plt.figure(figsize=(9, 4))
df['YM'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
plt.bar(df['YM'], df['SalesAmount'])
plt.xticks(rotation=60)
plt.title('AdventureWorks DW: Monthly Internet Sales')
plt.xlabel('Year-Month')
plt.ylabel('Sales Amount')
plt.tight_layout()
plt.savefig('dw_monthly_sales.png', dpi=150)
plt.show()

df.to_csv('dw_sales.csv', index=False, encoding='utf-8-sig')