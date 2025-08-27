import pandas as pd
import plotly.express as px

# 1. 데이터 불러오기
df = pd.read_csv('dw_sales.csv')

# 연-월 컬럼 생성
df['YM'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

# 2. 그래프 생성
fig = px.line(
    df,
    x='YM',
    y='SalesAmount',
    title='DW Monthly Sales (Interactive)',
    markers=True
)

# 3. 그래프 출력
fig.show()
