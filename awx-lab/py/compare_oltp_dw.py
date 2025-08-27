import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 불러오기
df_oltp = pd.read_csv('oltp_sales.csv')
df_dw = pd.read_csv('dw_sales.csv')

# 두 데이터프레임 병합 (Year, Month 기준)
df_merge = pd.merge(
    df_oltp, df_dw,
    on=['Year', 'Month'],
    suffixes=('_OLTP', '_DW')
)

# 매출 차이 계산
df_merge['Diff'] = df_merge['SalesAmount_OLTP'] - df_merge['SalesAmount_DW']

# 연-월 컬럼 생성
df_merge['YM'] = df_merge['Year'].astype(str) + '-' + df_merge['Month'].astype(str).str.zfill(2)

# 비교 시각화
plt.figure(figsize=(12, 6))
plt.plot(df_merge['YM'], df_merge['SalesAmount_OLTP'], marker='o', label='OLTP Sales')
plt.plot(df_merge['YM'], df_merge['SalesAmount_DW'], marker='x', label='DW Sales')
plt.xticks(rotation=60)
plt.title('OLTP vs DW: Monthly Sales Comparison')
plt.xlabel('Year-Month')
plt.ylabel('Sales Amount')
plt.legend()
plt.tight_layout()
plt.savefig('oltp_vs_dw_sales.png', dpi=150)
plt.show()

# 차이 확인
print("\n==== 매출 비교 ====")
print(df_merge[['YM', 'SalesAmount_OLTP', 'SalesAmount_DW', 'Diff']].head(10))
