import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# 데이터 읽기
df = pd.read_csv("war_data_world_war_1.csv")

# KM 분석을 위한 객체 생성
kmf_pre = KaplanMeierFitter()
kmf_post = KaplanMeierFitter()

# pre_ww1 그룹에 대한 분석
kmf_pre.fit(
    durations=df[df["pre_ww1"] == 1]["duration"],
    event_observed=~df[df["pre_ww1"] == 1]["is_censored"],
    label="Pre-WW1",
)

# post_ww1 그룹에 대한 분석
kmf_post.fit(
    durations=df[df["pre_ww1"] == 0]["duration"],
    event_observed=~df[df["pre_ww1"] == 0]["is_censored"],
    label="Post-WW1",
)

# 그래프 생성
plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

# KM 곡선 그리기
kmf_pre.plot(ax=ax, ci_show=True)
kmf_post.plot(ax=ax, ci_show=True)

# at-risk 수 추가
from lifelines.plotting import add_at_risk_counts

add_at_risk_counts(kmf_pre, kmf_post, ax=ax)

# 그래프 꾸미기
plt.title("Kaplan-Meier Survival Curves for Wars Before and After WW1")
plt.xlabel("Duration (Years)")
plt.ylabel("Survival Probability")
plt.grid(True)

# 각 그룹의 Life Table과 누적 생존율 출력
print("\nLife Table with Confidence Intervals for Pre-WW1 Wars:")
pre_table_with_ci = pd.concat(
    [kmf_pre.event_table, kmf_pre.survival_function_, kmf_pre.confidence_interval_],
    axis=1,
)
pre_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "survival_probability",
    "ci_lower",
    "ci_upper",
]
print(pre_table_with_ci)

print("\nLife Table with Confidence Intervals for Post-WW1 Wars:")
post_table_with_ci = pd.concat(
    [kmf_post.event_table, kmf_post.survival_function_, kmf_post.confidence_interval_],
    axis=1,
)
post_table_with_ci.columns = [
    "removed",
    "observed",
    "censored",
    "entrance",
    "at_risk",
    "survival_probability",
    "ci_lower",
    "ci_upper",
]
print(post_table_with_ci)

# 통계적 비교를 위한 로그순위 검정
from lifelines.statistics import logrank_test

durations_pre = df[df["pre_ww1"] == 1]["duration"]
durations_post = df[df["pre_ww1"] == 0]["duration"]
events_pre = ~df[df["pre_ww1"] == 1]["is_censored"]
events_post = ~df[df["pre_ww1"] == 0]["is_censored"]

results = logrank_test(durations_pre, durations_post, events_pre, events_post)
print(f"\nLog-rank test p-value: {results.p_value:.4f}")

# Cox 비례위험모형 분석
from lifelines import CoxPHFitter

# Cox 모델 생성
cph = CoxPHFitter()

# 데이터 준비
analysis_df = df[["duration", "pre_ww1"]].copy()
analysis_df["event"] = ~df["is_censored"]

# Cox 모델 적합
cph.fit(
    analysis_df,
    duration_col="duration",
    event_col="event",
    robust=True,
    show_progress=True,
)

# Cox 모델 결과 출력
print("\nCox Proportional Hazard Model Results:")
print(cph.print_summary())

# 위험비(Hazard Ratio) 계산 및 출력
coef_name = cph.params_.index[0]
print(f"Coefficient name: {coef_name}")
hazard_ratio = np.exp(cph.params_[coef_name])
print(f"\nHazard Ratio (Pre-WW1 vs Post-WW1): {hazard_ratio:.4f}")

# Life Table을 CSV 파일로 저장
pre_table_with_ci.to_csv("pre_ww1_life_table.csv")
post_table_with_ci.to_csv("post_ww1_life_table.csv")

plt.show()
