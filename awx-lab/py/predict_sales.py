import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 데이터 불러오기 (DW 월별 매출)
df = pd.read_csv('dw_sales.csv')

# 연-월 컬럼 생성 (YYYY-MM)
df['YM'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

# 월 번호 계산 (예: 첫 달 = 1, 그 다음 달 = 2, ...)
df['MonthIndex'] = np.arange(1, len(df) + 1)

# 특징(X)과 타깃(y) 정의
X = df[['MonthIndex']]      # 입력값
y = df['SalesAmount']       # 실제 매출액

# 2. 모델 학습
model = LinearRegression()
model.fit(X, y)

# 3. 예측 (기존 데이터 + 향후 12개월)
future_months = np.arange(1, len(df) + 13).reshape(-1, 1)
predictions = model.predict(future_months)

# 4. 평가
y_pred_existing = model.predict(X)
rmse = np.sqrt(mean_squared_error(y, y_pred_existing))
r2 = r2_score(y, y_pred_existing)
print(f"모델 평가: RMSE={rmse:.2f}, R²={r2:.4f}")

# 5. 시각화
plt.figure(figsize=(12, 6))
plt.plot(df['MonthIndex'], y, marker='o', label='Actual Sales')
plt.plot(future_months, predictions, linestyle='--', color='red', label='Predicted Sales')
plt.title('Monthly Sales Prediction (DW Data)')
plt.xlabel('Month Index')
plt.ylabel('Sales Amount')
plt.legend()
plt.tight_layout()
plt.savefig('predicted_sales.png', dpi=150)
plt.show()
