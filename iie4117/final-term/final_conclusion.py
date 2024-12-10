"""
고령화 종합 위험도 평가 및 정책 제언

이 파일은 앞선 세 가지 분석을 종합하여:
1. 산업별 고령화 위험도 평가
2. 산업 특성별 맞춤형 대응 전략
3. 정책적 제언
을 제시합니다.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
from time_series_analysis import load_and_preprocess_data

# 한글 폰트 설정
plt.style.use("seaborn")
plt.rcParams["font.family"] = "Malgun Gothic"


def calculate_risk_scores(trend_df):
    """산업별 고령화 위험도 점수 계산"""
    # 2023년 기준 데이터 추출
    current_data = trend_df[trend_df["연도"] == 2023].copy()

    # 고령화 속도 계산 (2012-2023)
    slopes = {}
    for industry in trend_df["산업"].unique():
        industry_data = trend_df[trend_df["산업"] == industry]
        if len(industry_data) > 1:
            slope, _, _, _, _ = stats.linregress(
                industry_data["연도"], industry_data["고령화율"]
            )
            slopes[industry] = slope

    current_data["고령화속도"] = current_data["산업"].map(slopes)

    # 위험도 점수 계산
    risk_factors = pd.DataFrame(index=current_data["산업"])
    scaler = MinMaxScaler(feature_range=(0, 100))

    # 1. 현재 고령화율 (0-100점)
    risk_factors["현재_고령화_위험도"] = scaler.fit_transform(
        current_data[["고령화율"]].values
    )

    # 2. 고령화 속도 위험도 (0-100점)
    risk_factors["변화_속도_위험도"] = scaler.fit_transform(
        current_data[["고령화속도"]].values
    )

    # 3. 산업 규모 위험도 (0-100점)
    risk_factors["규모_위험도"] = scaler.fit_transform(
        current_data[["전체근로자"]].values
    )

    # 4. 대체인력 확보 위험도 (0-100점)
    risk_factors["대체인력_위험도"] = scaler.fit_transform(
        (current_data["고령근로자"] / current_data["전체근로자"] * 100).values.reshape(
            -1, 1
        )
    )

    # 종합 위험도 계산 (가중치 적용)
    weights = {
        "현재_고령화_위험도": 0.3,
        "변화_속도_위험도": 0.3,
        "규모_위험도": 0.2,
        "대체인력_위험도": 0.2,
    }

    risk_factors["종합_위험도"] = sum(
        risk_factors[factor] * weight for factor, weight in weights.items()
    )

    return risk_factors, current_data


def visualize_risk_assessment(risk_factors):
    """위험도 평가 시각화"""
    # 1. 종합 위험도 히트맵
    plt.figure(figsize=(15, 8))
    risk_heatmap = risk_factors.sort_values("종합_위험도", ascending=False)

    sns.heatmap(
        risk_heatmap,
        cmap="RdYlGn_r",
        annot=True,
        fmt=".1f",
        cbar_kws={"label": "위험도 점수"},
    )

    plt.title("산업별 고령화 위험도 평가")
    plt.tight_layout()
    plt.show()

    # 2. 위험도 요인별 방사형 차트 (상위 5개 산업)
    top_industries = risk_factors.nlargest(5, "종합_위험도")

    categories = ["현재 고령화", "변화 속도", "산업 규모", "대체인력"]
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))  # 닫힌 다각형을 위해

    for idx, (industry, scores) in enumerate(top_industries.iterrows()):
        values = [
            scores["현재_고령화_위험도"],
            scores["변화_속도_위험도"],
            scores["규모_위험도"],
            scores["대체인력_위험도"],
        ]
        values = np.concatenate((values, [values[0]]))

        ax.plot(angles, values, "o-", linewidth=2, label=f"{industry[:15]}...")
        ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title("상위 5개 고위험 산업의 위험 요인 분석")
    plt.legend(bbox_to_anchor=(0.95, 0.95))
    plt.tight_layout()
    plt.show()


def generate_recommendations(risk_factors, current_data):
    """산업별 맞춤형 대응 전략 생성"""
    recommendations = {}

    for industry in risk_factors.index:
        scores = risk_factors.loc[industry]
        current = current_data[current_data["산업"] == industry].iloc[0]
        strategies = []

        # 1. 현재 고령화 대응
        if scores["현재_고령화_위험도"] > 75:
            strategies.append(
                f"즉시 대체인력 확보 필요 (현재 고령화율: {current['고령화율']:.1f}%)"
            )
        elif scores["현재_고령화_위험도"] > 50:
            strategies.append("단계적 인력구조 개선")

        # 2. 변화 속도 대응
        if scores["변화_속도_위험도"] > 75:
            strategies.append(
                f"청년 인력 유입 촉진 시급 (연간 증가율: {current['고령화속도']:.2f}%p)"
            )
        elif scores["변화_속도_위험도"] > 50:
            strategies.append("직무 재설계 검토")

        # 3. 규모 대응
        if scores["규모_위험도"] > 75:
            strategies.append(
                f"산업 전반의 구조조정 검토 (현재 근로자: {current['전체근로자']:,}명)"
            )
        elif scores["규모_위험도"] > 50:
            strategies.append("생산성 향상 방안 모색")

        # 4. 대체인력 대응
        if scores["대체인력_위험도"] > 75:
            strategies.append("외국인력 활용 검토")
        elif scores["대체인력_위험도"] > 50:
            strategies.append("교육훈련 체계 개선")

        recommendations[industry] = strategies

    return recommendations


def main():
    # 1. 데이터 로드
    print("시계열 분석 데이터 로드 중...")
    trend_df = load_and_preprocess_data()

    # 2. 위험도 평가
    print("\n산업별 위험도 평가 중...")
    risk_factors, current_data = calculate_risk_scores(trend_df)

    # 3. 위험도 시각화
    print("\n위험도 평가 결과 시각화...")
    visualize_risk_assessment(risk_factors)

    # 4. 대응 전략 생성
    print("\n산업별 맞춤형 대응 전략 생성 중...")
    recommendations = generate_recommendations(risk_factors, current_data)

    # 5. 결과 출력
    print("\n=== 고령화 위험도 평가 결과 ===")
    for industry in risk_factors.nlargest(5, "종합_위험도").index:
        print(f"\n{industry}")
        print(f"종합 위험도: {risk_factors.loc[industry, '종합_위험도']:.1f}점")
        print("권장 대응 전략:")
        for idx, strategy in enumerate(recommendations[industry], 1):
            print(f"  {idx}. {strategy}")


if __name__ == "__main__":
    main()
