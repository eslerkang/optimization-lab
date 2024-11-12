import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# 데이터 읽기
df = pd.read_csv("war_data_by_weapon.csv")

# KaplanMeierFitter 객체 생성
kmf = KaplanMeierFitter()

# 그래프 스타일 설정
plt.figure(figsize=(12, 8))

# 각 무기체계 시대별 색상 지정
colors = ["blue", "green", "red", "purple", "orange"]
weapon_labels = {
    1: "재래식 무기 시대 (1803-1850)",
    2: "산업화 무기 시대 (1851-1913)",
    3: "기계화 전쟁 시대 (1914-1944)",
    4: "핵무기 시대 (1945-1990)",
    5: "정밀 타격 시대 (1991-현재)",
}

# 각 무기체계 시대별로 분석
for era in sorted(df["weapon_era"].unique()):
    mask = df["weapon_era"] == era
    kmf.fit(
        durations=df[mask]["duration"],
        event_observed=~df[mask]["is_censored"],
        label=weapon_labels[era],
    )
    kmf.plot(ci_show=True, color=colors[era - 1])

# 그래프 꾸미기
plt.title("Kaplan-Meier Survival Curves by Weapon System Era")
plt.xlabel("Duration (Years)")
plt.ylabel("Survival Probability")
plt.grid(True)

# 통계적 비교를 위한 로그순위 검정
from lifelines.statistics import logrank_test

print("\nLog-rank test results:")
eras = sorted(df["weapon_era"].unique())
for i in range(len(eras)):
    for j in range(i + 1, len(eras)):
        era1, era2 = eras[i], eras[j]
        mask1 = df["weapon_era"] == era1
        mask2 = df["weapon_era"] == era2

        results = logrank_test(
            df[mask1]["duration"],
            df[mask2]["duration"],
            ~df[mask1]["is_censored"],
            ~df[mask2]["is_censored"],
        )
        print(f"{weapon_labels[era1]} vs {weapon_labels[era2]}")
        print(f"p-value: {results.p_value:.4f}\n")

# 각 시대별 중앙 생존 시간(median survival time) 계산
print("\nMedian survival time by era:")
for era in sorted(df["weapon_era"].unique()):
    mask = df["weapon_era"] == era
    kmf.fit(durations=df[mask]["duration"], event_observed=~df[mask]["is_censored"])
    median = kmf.median_survival_time_
    print(f"{weapon_labels[era]}: {median:.1f} years")

plt.show()
