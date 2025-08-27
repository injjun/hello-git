import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# 환경변수 로드
load_dotenv()

SERVER = os.getenv("SQL_SERVER", "localhost")
PORT = os.getenv("SQL_PORT", "1433")
DB = os.getenv("SQL_DB_OLTP", "AdventureWorks2022")
AUTH = os.getenv("SQL_AUTH", "windows").lower()
USER = os.getenv("SQL_USERNAME")
PWD = os.getenv("SQL_PASSWORD")

# ODBC 연결 설정 (현재 환경은 ODBC Driver 17)
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
WITH SalesCTE AS (
    SELECT
        YEAR(soh.OrderDate) AS [Year],
        MONTH(soh.OrderDate) AS [Month],
        SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS SalesAmount
    FROM Sales.SalesOrderHeader AS soh
    JOIN Sales.SalesOrderDetail AS sod
        ON soh.SalesOrderID = sod.SalesOrderID
    GROUP BY YEAR(soh.OrderDate), MONTH(soh.OrderDate)
)
SELECT [Year], [Month], CAST(SalesAmount AS DECIMAL(18,2)) AS SalesAmount
FROM SalesCTE
ORDER BY [Year], [Month];
"""

# DB 연결 및 데이터 조회
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(sql, conn)

# 시각화
plt.figure(figsize=(9, 4))
df['YM'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
plt.plot(df['YM'], df['SalesAmount'], marker='o')
plt.xticks(rotation=60)
plt.title('AdventureWorks OLTP: Monthly Sales')
plt.xlabel('Year-Month')
plt.ylabel('Sales Amount')
plt.tight_layout()
plt.savefig('oltp_monthly_sales.png', dpi=150)
plt.show()

df.to_csv('oltp_sales.csv', index=False, encoding='utf-8-sig')