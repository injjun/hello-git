# viz.py
# 임의의 데이터로 선 그래프를 그려 현재 폴더에 viz.png로 저장합니다.

import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경에서 이미지 저장을 위해 Agg 백엔드 사용
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import random


def main():
    out_dir = Path(__file__).parent

    # 샘플 날짜와 값 생성 (12개월)
    dates = pd.date_range(start='2025-01-01', periods=12, freq='M')
    random.seed(0)
    values = [100 + random.random() * 50 + i * 5 for i in range(len(dates))]

    df = pd.DataFrame({'date': dates, 'value': values})

    # 그래프 그리기
    plt.figure(figsize=(8, 4))
    plt.plot(df['date'], df['value'], marker='o', linestyle='-')
    plt.title('샘플 선그래프')
    plt.xlabel('날짜')
    plt.ylabel('값')
    plt.grid(True)
    plt.tight_layout()

    out_path = out_dir / 'viz.png'
    plt.savefig(out_path)
    print(f'이미지 저장: {out_path}')


if __name__ == '__main__':
    main()
