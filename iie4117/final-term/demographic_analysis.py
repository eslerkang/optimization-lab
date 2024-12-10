"""
전체 인구 동향 분석 (Demographic Analysis)

이 파일은 대한민국의 전반적인 인구 구조 변화를 분석합니다.
주요 분석 내용:
1. 생산가능인구(15-64세)와 고령인구(65세 이상) 추세 비교 (2024-2072)
2. 노년부양비 추세 분석
3. 인구구조 변화에 따른 노동시장 영향 예측
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"

# 1. 인구 예측 데이터 로드
pop_pred = pd.read_csv("population_pred.csv")

# 2. 외요 지표 추출 (콤마 제거 후 float 변환)
years = pop_pred.columns[1:].astype(int)
working_age = (
    pop_pred[pop_pred["인구종류별"] == "생산연령인구(천명): 계(15~64세)"]
    .iloc[0, 1:]
    .apply(lambda x: float(str(x).replace(",", "")))
)
elderly = (
    pop_pred[pop_pred["인구종류별"] == "고령인구(천명): 65세+"]
    .iloc[0, 1:]
    .apply(lambda x: float(str(x).replace(",", "")))
)

# 3. 생산가능인구 vs 고령인구 추세 시각화
plt.figure(figsize=(15, 8))
plt.plot(years, working_age / 1000, label="생산가능인구", marker="o")
plt.plot(years, elderly / 1000, label="고령인구", marker="o")
plt.title("생산가능인구 vs 고령인구 추세 (2024-2072)")
plt.xlabel("연도")
plt.ylabel("인구 (백만명)")
plt.grid(True)
plt.legend()
plt.xticks(years[::5], rotation=45)
plt.tight_layout()
plt.show()

# 4. 노년부양비 계산 및 시각화
dependency_ratio = (elderly / working_age) * 100

plt.figure(figsize=(15, 8))
plt.plot(years, dependency_ratio, label="노년부양비", marker="o", color="red")
plt.title("노년부양비 추세 (2024-2072)")
plt.xlabel("연도")
plt.ylabel("노년부양비 (%)")
plt.grid(True)
plt.legend()
plt.xticks(years[::5], rotation=45)
plt.tight_layout()
plt.show()

# 5. 주요 변곡점 분석
critical_years = []
for i in range(1, len(years) - 1):
    if (dependency_ratio.iloc[i] - dependency_ratio.iloc[i - 1]) > (
        dependency_ratio.iloc[i + 1] - dependency_ratio.iloc[i]
    ):
        critical_years.append((years[i], dependency_ratio.iloc[i]))

# 6. 분석 결과 출력
print("\n=== 인구구조 변화 분석 결과 ===")
print(f"\n1. 생산가능인구 변화")
print(f"- 2024년: {working_age.iloc[0]/1000:.1f}백만명")
print(f"- 2072년: {working_age.iloc[-1]/1000:.1f}백만명")
print(
    f"- 감소율: {((working_age.iloc[-1] - working_age.iloc[0])/working_age.iloc[0])*100:.1f}%"
)

print(f"\n2. 고령인구 변화")
print(f"- 2024년: {elderly.iloc[0]/1000:.1f}백만명")
print(f"- 2072년: {elderly.iloc[-1]/1000:.1f}백만명")
print(f"- 증가율: {((elderly.iloc[-1] - elderly.iloc[0])/elderly.iloc[0])*100:.1f}%")

print(f"\n3. 노년부양비 변화")
print(f"- 2024년: {dependency_ratio.iloc[0]:.1f}%")
print(f"- 2072년: {dependency_ratio.iloc[-1]:.1f}%")
print(f"- 주요 변곡점:")
for year, ratio in critical_years:
    print(f"  * {year}년: {ratio:.1f}%")

print("\n4. 노동시장 영향 예측")
print("- 생산가능인구 감소로 인한 노동력 부족 심화")
print("- 노년부양비 증가로 인한 사회보장 부담 증가")
print("- 산업 전반의 인력수급 어려움 예상")
