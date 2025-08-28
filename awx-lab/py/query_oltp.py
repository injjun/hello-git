# query_dw.py
import os, urllib.parse
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1) .env 로드
load_dotenv(find_dotenv(), override=True)

SERVER = os.getenv("SQL_SERVER", r"localhost\SQLEXPRESS")
PORT   = os.getenv("SQL_PORT", "1433")
DB     = os.getenv("SQL_DB_DW", "AdventureWorksDW2022")
USER   = os.getenv("SQL_USERNAME")          # 예: sa 또는 appuser
PWD    = os.getenv("SQL_PASSWORD")

# 2) ODBC 연결 문자열 (SQL 로그인 사용)
odbc = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER},{PORT};DATABASE={DB};"
    f"UID={USER};PWD={PWD};"
    f"Encrypt=yes;TrustServerCertificate=yes;"
)
params = urllib.parse.quote_plus(odbc)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 3) 쿼리
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

# 4) 실행 & 시각화
with engine.begin() as conn:
    who = pd.read_sql_query(
        "SELECT @@SERVERNAME AS ServerName, SUSER_SNAME() AS LoginName;", conn
    )
    print(who)
    df = pd.read_sql_query(sql, conn)

plt.figure(figsize=(9, 4))
df["YM"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
plt.bar(df["YM"], df["SalesAmount"])
plt.xticks(rotation=60)
plt.title("AdventureWorks DW: Monthly Internet Sales")
plt.xlabel("Year-Month")
plt.ylabel("Sales Amount")
plt.tight_layout()
plt.savefig("dw_monthly_sales.png", dpi=150)
plt.show()

df.to_csv("dw_sales.csv", index=False, encoding="utf-8-sig")
