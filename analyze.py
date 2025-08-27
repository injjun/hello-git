import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
print(df)

print("\n기초 통계:")
print(df["value"].describe())

ax = df.plot(x="day", y="value", kind="line", marker="o", title="Values by Day")
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("chart.png")
print("Saved chart.png")


