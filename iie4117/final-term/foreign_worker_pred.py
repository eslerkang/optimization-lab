import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet

# plt.style.use("seaborn")
plt.rcParams["font.family"] = "Malgun Gothic"

# 데이터 로드
foreign_worker = pd.read_csv("datas/foreign_worker_by_year.csv")
foreign_worker["total"] = foreign_worker["total"] * 10000  # 만 단위로 저장된 경우

# Prophet 모델을 위한 데이터 준비 - 연도를 날짜 형식으로 변환
df = pd.DataFrame(
    {
        "ds": pd.to_datetime(foreign_worker["year"].astype(str) + "-01-01"),
        "y": foreign_worker["total"],
    }
)

# Prophet 모델 생성 및 학습 - 최소값 0으로 제약 설정
model = Prophet(yearly_seasonality=True, growth="logistic")  # 로지스틱 성장 모델 사용

# 최소값을 0으로 설정
df["cap"] = df["y"].max() * 2  # 최대값은 현재 최대값의 2배로 설정
df["floor"] = 0  # 최소값은 0으로 설정

model.fit(df)

# 2072년까지 예측
future_dates = pd.date_range(start="2024-01-01", end="2072-12-31", freq="Y")
future = pd.DataFrame({"ds": future_dates})
future["cap"] = df["cap"].max()  # 미래 데이터에도 같은 최대값 적용
future["floor"] = 0  # 미래 데이터에도 최소값 0 적용

forecast = model.predict(future)

# 결과 시각화
plt.figure(figsize=(15, 8))
plt.plot(df["ds"], df["y"], "b-", label="실제 데이터")
plt.plot(forecast["ds"], forecast["yhat"], "r--", label="예측 데이터")
plt.fill_between(
    forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="r", alpha=0.1
)

plt.title("외국인 근로자 수 예측 (2011-2072)")
plt.xlabel("연도")
plt.ylabel("외국인 근로자 수 (명)")
plt.legend()
plt.grid(True)

# y축 범위 설정 - 0 이상만 표시
plt.ylim(bottom=0)

# 주요 시점별 예측값 출력
print("\n=== 주요 시점별 외국인 근로자 수 예측 ===")
key_years = [2030, 2040, 2050, 2060, 2072]
for year in key_years:
    value = forecast[forecast["ds"].dt.year == year]["yhat"].values[0]
    lower = forecast[forecast["ds"].dt.year == year]["yhat_lower"].values[0]
    upper = forecast[forecast["ds"].dt.year == year]["yhat_upper"].values[0]
    # 음수값이 있으면 0으로 조정
    lower = max(0, lower)
    print(f"{year}년: {value:,.0f}명 (95% 신뢰구간: {lower:,.0f}명 ~ {upper:,.0f}명)")

plt.tight_layout()
plt.show()
