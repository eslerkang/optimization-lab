import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# 데이터 읽기
df = pd.read_csv("war_data_world.csv")

# KM 분석을 위한 객체 생성
kmf_pre_ww1 = KaplanMeierFitter()
kmf_post_ww1 = KaplanMeierFitter()

# pre_ww1 그룹에 대한 분석
kmf_pre_ww1.fit(
    durations=df[df["pre_ww1"] == 1]["duration"],
    event_observed=df[df["pre_ww1"] == 1]["is_censored"].map(lambda x: not x),
    label="Pre-WW1",
)

# post_ww1 그룹에 대한 분석
kmf_post_ww1.fit(
    durations=df[df["pre_ww1"] == 0]["duration"],
    event_observed=df[df["pre_ww1"] == 0]["is_censored"].map(lambda x: not x),
    label="Post-WW1",
)

# WW2 분석
kmf_pre_ww2 = KaplanMeierFitter()
kmf_post_ww2 = KaplanMeierFitter()

kmf_pre_ww2.fit(
    durations=df[df["pre_ww2"] == 1]["duration"],
    event_observed=df[df["pre_ww2"] == 1]["is_censored"].map(lambda x: not x),
    label="Pre-WW2",
)
kmf_post_ww2.fit(
    durations=df[df["pre_ww2"] == 0]["duration"],
    event_observed=df[df["pre_ww2"] == 0]["is_censored"].map(lambda x: not x),
    label="Post-WW2",
)

# 지역별 분석
regions = [
    "europe",
    "east_asia",
    "southeast_asia",
    "middle_east",
    "africa",
    "north_america",
    "south_america",
    "central_asia",
    "south_asia",
]

regional_kmf = {}
for region in regions:
    kmf = KaplanMeierFitter()
    kmf.fit(
        durations=df[df[region] == 1]["duration"],
        event_observed=df[df[region] == 1]["is_censored"].map(lambda x: not x),
        label=region.replace("_", " ").title(),
    )
    regional_kmf[region] = kmf

# 그래프 생성
plt.figure(figsize=(20, 16))

# WW1 분석 그래프
plt.subplot(221)
kmf_pre_ww1.plot(ci_show=True)
kmf_post_ww1.plot(ci_show=True)

# WW1 중앙값 표시
median_pre_ww1 = kmf_pre_ww1.median_survival_time_
median_post_ww1 = kmf_post_ww1.median_survival_time_
plt.axvline(x=median_pre_ww1, color="blue", linestyle="--", alpha=0.5)
plt.axvline(x=median_post_ww1, color="orange", linestyle="--", alpha=0.5)
plt.axhline(y=0.5, color="gray", linestyle="--", alpha=0.3)
plt.text(
    median_pre_ww1, 0.55, f"Median: {median_pre_ww1:.1f}y", rotation=90, color="blue"
)
plt.text(
    median_post_ww1,
    0.55,
    f"Median: {median_post_ww1:.1f}y",
    rotation=90,
    color="orange",
)

plt.title("Wars Before and After WW1")
plt.xlabel("Duration (Years)")
plt.ylabel("Survival Probability")
plt.grid(True)

# WW2 분석 그래프
plt.subplot(222)
kmf_pre_ww2.plot(ci_show=True)
kmf_post_ww2.plot(ci_show=True)

# WW2 중앙값 표시
median_pre_ww2 = kmf_pre_ww2.median_survival_time_
median_post_ww2 = kmf_post_ww2.median_survival_time_
plt.axvline(x=median_pre_ww2, color="blue", linestyle="--", alpha=0.5)
plt.axvline(x=median_post_ww2, color="orange", linestyle="--", alpha=0.5)
plt.axhline(y=0.5, color="gray", linestyle="--", alpha=0.3)
plt.text(
    median_pre_ww2, 0.55, f"Median: {median_pre_ww2:.1f}y", rotation=90, color="blue"
)
plt.text(
    median_post_ww2,
    0.55,
    f"Median: {median_post_ww2:.1f}y",
    rotation=90,
    color="orange",
)

plt.title("Wars Before and After WW2")
plt.xlabel("Duration (Years)")
plt.ylabel("Survival Probability")
plt.grid(True)

plt.tight_layout()
plt.show()

# 중앙값 출력
print("\nMedian Survival Times:")
print(f"Pre-WW1:  {median_pre_ww1:.2f} years")
print(f"Post-WW1: {median_post_ww1:.2f} years")
print(f"Pre-WW2:  {median_pre_ww2:.2f} years")
print(f"Post-WW2: {median_post_ww2:.2f} years")

# 지역별 분석을 위한 새로운 그래프
plt.figure(figsize=(15, 10))

# 그래프를 위한 서브플롯 생성 및 여백 조정
plt.subplots_adjust(right=0.80)  # 오른쪽 여백을 더 늘림

for region in regions:
    regional_kmf[region].plot(ci_show=False)

    # 각 지역의 중앙값 위치에 수직선만 표시
    median = regional_kmf[region].median_survival_time_
    plt.axvline(x=median, linestyle="--", alpha=0.3)

plt.axhline(y=0.5, color="gray", linestyle="--", alpha=0.3)
plt.title("Wars by Region")
plt.xlabel("Duration (Years)")
plt.ylabel("Survival Probability")
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

# 중앙값 정보를 그래프 오른쪽에 텍스트로 표시
medians_text = "Median Survival Times:\n"
for region in regions:
    median = regional_kmf[region].median_survival_time_
    medians_text += f"{region.replace('_', ' ').title():15}: {median:.1f} years\n"

plt.figtext(0.83, 0.5, medians_text, fontsize=10, family="monospace", va="center")

plt.show()

# 지역별 중앙값 출력
print("\nMedian Survival Times by Region:")
for region in regions:
    median = regional_kmf[region].median_survival_time_
    print(f"{region.replace('_', ' ').title():15} {median:.2f} years")

# WW1 Life Table 출력
print("\nLife Table with Confidence Intervals for Pre-WW1 Wars:")
pre_ww1_table_with_ci = pd.concat(
    [
        kmf_pre_ww1.event_table,
        kmf_pre_ww1.survival_function_,
        kmf_pre_ww1.confidence_interval_,
    ],
    axis=1,
)
pre_ww1_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "cumulative_survival_probability",
    "ci_lower",
    "ci_upper",
]
print(pre_ww1_table_with_ci)

print("\nLife Table with Confidence Intervals for Post-WW1 Wars:")
post_ww1_table_with_ci = pd.concat(
    [
        kmf_post_ww1.event_table,
        kmf_post_ww1.survival_function_,
        kmf_post_ww1.confidence_interval_,
    ],
    axis=1,
)
post_ww1_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "cumulative_survival_probability",
    "ci_lower",
    "ci_upper",
]
print(post_ww1_table_with_ci)

# WW2 Life Table 출력
print("\nLife Table with Confidence Intervals for Pre-WW2 Wars:")
pre_ww2_table_with_ci = pd.concat(
    [
        kmf_pre_ww2.event_table,
        kmf_pre_ww2.survival_function_,
        kmf_pre_ww2.confidence_interval_,
    ],
    axis=1,
)
pre_ww2_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "cumulative_survival_probability",
    "ci_lower",
    "ci_upper",
]
print(pre_ww2_table_with_ci)

print("\nLife Table with Confidence Intervals for Post-WW2 Wars:")
post_ww2_table_with_ci = pd.concat(
    [
        kmf_post_ww2.event_table,
        kmf_post_ww2.survival_function_,
        kmf_post_ww2.confidence_interval_,
    ],
    axis=1,
)
post_ww2_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "cumulative_survival_probability",
    "ci_lower",
    "ci_upper",
]
print(post_ww2_table_with_ci)

pre_ww1_table_with_ci.to_csv("life_table_pre_ww1.csv")
post_ww1_table_with_ci.to_csv("life_table_post_ww1.csv")
pre_ww2_table_with_ci.to_csv("life_table_pre_ww2.csv")
post_ww2_table_with_ci.to_csv("life_table_post_ww2.csv")

print("\nLife tables have been saved to CSV files:")
print("- life_table_pre_ww1.csv")
print("- life_table_post_ww1.csv")
print("- life_table_pre_ww2.csv")
print("- life_table_post_ww2.csv")

# 통계적 비교를 위한 로그순위 검정
print("\nLog-rank test results:")

# WW1 전후 비교
results_ww1 = logrank_test(
    df[df["pre_ww1"] == 1]["duration"],
    df[df["pre_ww1"] == 0]["duration"],
    df[df["pre_ww1"] == 1]["is_censored"].map(lambda x: not x),
    df[df["pre_ww1"] == 0]["is_censored"].map(lambda x: not x),
)
print(f"WW1 comparison p-value: {results_ww1.p_value:.4f}")

# WW2 전후 비교
results_ww2 = logrank_test(
    df[df["pre_ww2"] == 1]["duration"],
    df[df["pre_ww2"] == 0]["duration"],
    df[df["pre_ww2"] == 1]["is_censored"].map(lambda x: not x),
    df[df["pre_ww2"] == 0]["is_censored"].map(lambda x: not x),
)
print(f"WW2 comparison p-value: {results_ww2.p_value:.4f}")

# Cox 비례위험모형 분석
from lifelines import CoxPHFitter

# Cox 모델 생성
cph = CoxPHFitter()

# 모든 예측변수 정의
predictors = [
    "pre_ww1",
    "pre_ww2",
    "europe",
    "east_asia",
    "southeast_asia",
    "middle_east",
    "africa",
    "north_america",
    "south_america",
    "central_asia",
    "south_asia",
]

# 데이터 준비
analysis_df = df[["duration"] + predictors].copy()
analysis_df["event"] = df["is_censored"].map(lambda x: not x)

# Cox 모델 적합
cph.fit(
    analysis_df,
    duration_col="duration",
    event_col="event",
    robust=True,
    show_progress=True,
)

# Cox 모델 결과 력
print("\nCox Proportional Hazard Model Results:")
print(cph.print_summary())

# 각 변수의 위험비(Hazard Ratio) 계산 및 출력
print("\nHazard Ratios for all variables:")
for coef_name in cph.params_.index:
    hazard_ratio = np.exp(cph.params_[coef_name])
    p_value = cph.summary.loc[coef_name, "p"]
    print(f"{coef_name:15} HR: {hazard_ratio:.4f} (p-value: {p_value:.4f})")


plt.show()
