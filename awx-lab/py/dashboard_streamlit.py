import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 제목
st.title("📊 DW 월별 매출 대시보드")

# 1. 데이터 불러오기
df = pd.read_csv('dw_sales.csv')
df['YM'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

# 2. 필터 UI
years = df['Year'].unique()
selected_year = st.selectbox("연도를 선택하세요", years)

# 선택한 연도의 데이터 필터링
filtered_df = df[df['Year'] == selected_year]

# 3. 대화형 그래프
fig = px.bar(
    filtered_df,
    x='YM',
    y='SalesAmount',
    title=f'{selected_year}년 월별 매출',
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# 4. 데이터 테이블 표시
st.subheader("📋 데이터 테이블")
st.dataframe(filtered_df)
