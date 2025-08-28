import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# 1) 환경변수 로드
load_dotenv()

# 2) 환경 변수 가져오기
SERVER = os.getenv("SQL_SERVER", r"localhost\SQLEXPRESS")
PORT = os.getenv("SQL_PORT", "1433")
DB = os.getenv("SQL_DB_DW", "AdventureWorksDW2022")
USER = os.getenv("SQL_USERNAME")
PWD = os.getenv("SQL_PASSWORD")

# 3) SQL 로그인 연결 문자열
conn_str = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server={SERVER},{PORT};"
    f"Database={DB};"
    f"Uid={USER};Pwd={PWD};"
    f"Encrypt=yes;TrustServerCertificate=yes;"
)

# 4) SQL 쿼리
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

# 5) DB 연결 및 데이터 읽기
with pyodbc.connect(conn_str) as conn:
    who = pd.read_sql("SELECT @@SERVERNAME AS ServerName, SUSER_SNAME() AS LoginName;", conn)
    print("[INFO] 연결 성공:", who)
    df = pd.read_sql(sql, conn)

# 6) 시각화
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

# 7) CSV로 저장
df.to_csv('dw_sales.csv', index=False, encoding='utf-8-sig')
