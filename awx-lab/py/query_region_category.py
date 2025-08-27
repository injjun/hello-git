import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# .env 환경변수 불러오기
load_dotenv()

SERVER = os.getenv("SQL_SERVER", "localhost")
PORT = os.getenv("SQL_PORT", "1433")
DB = os.getenv("SQL_DB_DW", "AdventureWorksDW2022")
AUTH = os.getenv("SQL_AUTH", "windows").lower()
USER = os.getenv("SQL_USERNAME")
PWD = os.getenv("SQL_PASSWORD")

# ODBC 연결 문자열 (현재 ODBC Driver 17 사용)
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

# SQL 쿼리 불러오기
with open(r"..\sql\sales_by_region_category.sql", "r", encoding="utf-8") as file:
    query = file.read()

# DB 연결 및 데이터 조회
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(query, conn)

# 데이터 확인
print("\n=== 매출 상위 10개 ===")
print(df.head(10))

# 지역별로 상위 10개 제품만 집계
top_products = df.groupby('Product')['TotalSales'].sum().nlargest(10).index
df_top = df[df['Product'].isin(top_products)]

# 시각화
plt.figure(figsize=(14, 6))
for region in df_top['Region'].unique():
    subset = df_top[df_top['Region'] == region]
    plt.bar(subset['Product'], subset['TotalSales'], label=region)

plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Product Sales by Region')
plt.ylabel('Total Sales')
plt.legend()
plt.tight_layout()
plt.savefig('sales_by_region_category.png', dpi=150)
plt.show()
