"""
산업별 고령화 추세 분석 (Time Series Analysis)

이 파일은 2012-2023년 기간 동안의 산업별 고령화 추세를 분석합니다.
주요 분석 내용:
1. 산업별 고령화율 시계열 분석
   - 추세(Trend) 분석
   - 계절성(Seasonality) 확인
   - 변화 포인트(Change Point) 감지
2. 시계열 예측 모델링
   - ARIMA 모델 적용
3. 산업 클러스터링 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from ruptures import Binseg
import warnings

warnings.filterwarnings("ignore")

# 한글 폰트 및 스타일 설정
plt.style.use("seaborn")
plt.rcParams["font.family"] = "Malgun Gothic"


def load_and_preprocess_data():
    """데이터 로드 및 전처리"""
    # 데이터 로드
    elder_worker = pd.read_csv("elder_worker.csv")

    # 첫 번째 행을 제외하고 실제 데이터만 사용
    elder_worker = elder_worker.iloc[1:]

    # '소계' 행 제외
    elder_worker = elder_worker[elder_worker["구분별"] != "소계"]

    trend_data = []

    # 각 연도별 데이터 처리
    for year in range(2012, 2024):
        # 해당 연도의 컬럼들 찾기
        year_cols = [
            col for col in elder_worker.columns if str(year) == col.split(".")[0]
        ]
        if not year_cols or len(year_cols) < 3:  # 필요한 컬럼이 없으면 스킵
            continue

        # 전체 근로자와 55세 이상 근로자 컬럼 선택
        total_workers_col = year_cols[1]  # 전체 근로자
        elder_workers_col = year_cols[2]  # 55세 이상 근로자

        for _, row in elder_worker.iterrows():
            # 숫자 데이터 변환
            try:
                total_workers = pd.to_numeric(
                    str(row[total_workers_col]).replace(",", ""), errors="coerce"
                )
                elder_workers = pd.to_numeric(
                    str(row[elder_workers_col]).replace(",", ""), errors="coerce"
                )

                if (
                    pd.notna(total_workers)
                    and pd.notna(elder_workers)
                    and total_workers > 0
                ):
                    trend_data.append(
                        {
                            "연도": year,
                            "산업": row["구분별"],
                            "고령화율": (elder_workers / total_workers) * 100,
                            "전체근로자": total_workers,
                            "고령근로자": elder_workers,
                        }
                    )
            except:
                continue

    return pd.DataFrame(trend_data)


def calculate_aging_slopes(trend_df):
    """산업별 고령화 속도 계산"""
    slopes = {}
    for industry in trend_df["산업"].unique():
        industry_data = trend_df[trend_df["산업"] == industry]
        if len(industry_data) > 1:
            slope, _, _, _, _ = stats.linregress(
                industry_data["연도"], industry_data["고령화율"]
            )
            slopes[industry] = slope

    slopes_df = pd.DataFrame(list(slopes.items()), columns=["산업", "고령화속도"])
    return slopes_df.sort_values("고령화속도", ascending=False)


def plot_top_industries_trend(trend_df, slopes_df, n_industries=5):
    """상위 n개 산업의 고령화 추세 시각화"""
    plt.figure(figsize=(15, 8))

    top_industries = slopes_df.head(n_industries)["산업"].tolist()
    for industry in top_industries:
        industry_data = trend_df[trend_df["산업"] == industry].sort_values("연도")
        plt.plot(
            industry_data["연도"],
            industry_data["고령화율"],
            marker="o",
            label=f"{industry[:20]}...",
        )

    plt.title(f"고령화 진행 속도 상위 {n_industries}개 산업의 추세 (2012-2023)")
    plt.xlabel("연도")
    plt.ylabel("고령화율 (%)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def detect_change_points(data, n_bkps=2):
    """변화 포인트 감지"""
    if len(data) < 5:  # 데이터가 너무 적으면 빈 리스트 반환
        return []

    try:
        algo = Binseg(model="l2").fit(data.values.reshape(-1, 1))
        # 데이터 길이에 따라 변화점 개수 조정
        n_bkps = min(n_bkps, len(data) - 2)
        if n_bkps <= 0:
            return []
        change_points = algo.predict(n_bkps=n_bkps)
        return change_points
    except:
        return []


def analyze_time_series(trend_df, industry):
    """개별 산업의 시계열 분석"""
    industry_data = trend_df[trend_df["산업"] == industry].copy()
    industry_data = industry_data.sort_values("연도")

    # 시계열 분해
    try:
        decomposition = seasonal_decompose(
            industry_data["고령화율"], period=2, extrapolate_trend="freq"
        )

        fig, axes = plt.subplots(4, 1, figsize=(15, 12))

        # Original
        axes[0].plot(industry_data["연도"], industry_data["고령화율"])
        axes[0].set_title("Original")

        # Trend
        axes[1].plot(industry_data["연도"], decomposition.trend)
        axes[1].set_title("Trend")

        # Seasonal
        axes[2].plot(industry_data["연도"], decomposition.seasonal)
        axes[2].set_title("Seasonal")

        # Residual
        axes[3].plot(industry_data["연도"], decomposition.resid)
        axes[3].set_title("Residual")

        plt.suptitle(f"{industry} 시계열 분해 분석")
        plt.tight_layout()
        plt.show()
    except:
        print(f"{industry} 시계열 분해 실패 - 데이터 부족")

    # 변화 포인트 감지
    change_points = detect_change_points(industry_data["고령화율"])
    if change_points:
        change_years = [industry_data["연도"].iloc[cp] for cp in change_points[:-1]]

        print(f"\n{industry} 주요 변화 시점:")
        for year in change_years:
            rate = industry_data[industry_data["연도"] == year]["고령화율"].iloc[0]
            print(f"- {year}년: {rate:.1f}%")

    return None


def perform_clustering_analysis(trend_df, slopes_df):
    """산업 클러스터링 분석"""
    # 산업별 특성 추출
    industry_features = pd.DataFrame(
        {
            "평균고령화율": trend_df.groupby("산업")["고령화율"].mean(),
            "고령화속도": slopes_df.set_index("산업")["고령화속도"],
            "변동성": trend_df.groupby("산업")["고령화율"].std(),
        }
    )

    # NaN 값 처리
    industry_features = industry_features.dropna()  # NaN이 있는 행 제거

    if len(industry_features) < 4:  # 데이터가 너무 적으면 클러스터 수 조정
        n_clusters = max(2, len(industry_features) - 1)
    else:
        n_clusters = 4

    # 클러스터링
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(industry_features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    industry_features["클러스터"] = kmeans.fit_predict(scaled_features)

    # 시각화
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(
        industry_features["평균고령화율"],
        industry_features["고령화속도"],
        c=industry_features["클러스터"],
        s=industry_features["변동성"] * 100,
    )

    # 산업명 추가
    for idx, row in industry_features.iterrows():
        plt.annotate(
            idx[:10] + "...",
            (row["평균고령화율"], row["고령화속도"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

    plt.xlabel("평균 고령화율")
    plt.ylabel("고령화 속도")
    plt.title("산업 클러스터링 결과")
    plt.colorbar(scatter, label="클러스터")
    plt.tight_layout()
    plt.show()

    return industry_features


def forecast_with_arima(trend_df, industry, forecast_years=5):
    """ARIMA 모델을 사용한 미래 예측"""
    industry_data = trend_df[trend_df["산업"] == industry].sort_values("연도")

    try:
        # ARIMA 모델 적합
        model = ARIMA(industry_data["고령화율"], order=(1, 1, 1))
        model_fit = model.fit()

        # 미래 예측
        forecast = model_fit.forecast(steps=forecast_years)
        forecast_years_list = range(
            industry_data["연도"].max() + 1,
            industry_data["연도"].max() + forecast_years + 1,
        )

        # 신뢰구간 계산
        pred_conf = model_fit.get_forecast(forecast_years).conf_int()

        # 시각화
        plt.figure(figsize=(12, 6))

        # 실제 데이터
        plt.plot(
            industry_data["연도"],
            industry_data["고령화율"],
            label="실제 데이터",
            marker="o",
        )

        # 예측 데이터
        plt.plot(
            forecast_years_list, forecast, label="예측", linestyle="--", marker="s"
        )

        # 신뢰구간
        plt.fill_between(
            forecast_years_list,
            pred_conf.iloc[:, 0],
            pred_conf.iloc[:, 1],
            color="gray",
            alpha=0.2,
            label="95% 신뢰구간",
        )

        plt.title(f"{industry} 고령화율 예측 (ARIMA)")
        plt.xlabel("연도")
        plt.ylabel("고령화율 (%)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 예측 결과 출력
        print(f"\n{industry} 고령화율 예측:")
        for year, rate, lower, upper in zip(
            forecast_years_list, forecast, pred_conf.iloc[:, 0], pred_conf.iloc[:, 1]
        ):
            print(
                f"- {year}년: {rate:.1f}% (95% 신뢰구간: {lower:.1f}% ~ {upper:.1f}%)"
            )

        return forecast, pred_conf

    except Exception as e:
        print(f"{industry} ARIMA 예측 실패: {str(e)}")
        return None, None


def main():
    # 1. 데이터 로드 및 전처리
    print("데이터 로드 중...")
    trend_df = load_and_preprocess_data()

    # 데이터 확인
    print(f"\n분석 기간: {trend_df['연도'].min()}-{trend_df['연도'].max()}")
    print(f"분석 대상 산업 수: {trend_df['산업'].nunique()}")

    # 2. 고령화 속도 계산
    slopes_df = calculate_aging_slopes(trend_df)

    # 3. 상위 산업 추세 시각화
    plot_top_industries_trend(trend_df, slopes_df)

    # 4. 상위 5개 산업 시계열 분석 및 예측
    print("\n=== 상위 5개 산업 시계열 분석 및 예측 ===")
    top_industries = slopes_df.head()["산업"].tolist()
    for industry in top_industries:
        print(f"\n{industry} 분석 중...")
        analyze_time_series(trend_df, industry)
        forecast_with_arima(trend_df, industry)

    # 5. 클러스터링 분석
    industry_features = perform_clustering_analysis(trend_df, slopes_df)

    # 6. 분석 결과 출력
    print("\n=== 산업별 고령화 추세 분석 결과 ===")
    print("\n1. 고령화 진행 속도 상위 5개 산업")
    for _, row in slopes_df.head().iterrows():
        industry_data = trend_df[trend_df["산업"] == row["산업"]]
        first_year = industry_data.sort_values("연도").iloc[0]
        last_year = industry_data.sort_values("연도").iloc[-1]

        print(f"\n{row['산업']}:")
        print(f"- 연간 고령화율 증가: {row['고령화속도']:.2f}%p")
        print(f"- {first_year['연도']}년 고령화율: {first_year['고령화율']:.1f}%")
        print(f"- {last_year['연도']}년 고령화율: {last_year['고령화율']:.1f}%")
        print(f"- 전체 증가폭: {last_year['고령화율'] - first_year['고령화율']:.1f}%p")

    # 7. 클러스터 특성 분석
    print("\n2. 클러스터 특성 분석")
    n_clusters = len(industry_features["클러스터"].unique())
    for cluster in range(n_clusters):
        cluster_industries = industry_features[industry_features["클러스터"] == cluster]
        if len(cluster_industries) > 0:  # 클러스터에 산업이 있는 경우만 출력
            print(f"\n[클러스터 {cluster}]")
            print(f"- 산업 수: {len(cluster_industries)}")
            print(f"- 평균 고령화율: {cluster_industries['평균고령화율'].mean():.1f}%")
            print(
                f"- 평균 고령화 속도: {cluster_industries['고령화속도'].mean():.2f}%p/년"
            )
            print(f"- 대표 산업: {cluster_industries.index[0]}")


if __name__ == "__main__":
    main()
