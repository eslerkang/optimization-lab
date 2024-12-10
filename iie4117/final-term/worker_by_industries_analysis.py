import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")

# 데이터 로드
foreign_worker_by_industries = pd.read_csv("datas/foreign_worker_by_industries.csv")
elder_worker = pd.read_csv("datas/elder_worker.csv")

# 서비스업 관련 산업 리스트
service_industries = [
    "도매 및 소매업",
    "운수 및 창고업",
    "숙박 및 음식점업",
    "정보통신업",
    "금융 및 보험업",
    "부동산업",
    "전문, 과학 및 기술 서비스업",
    "사업시설 관리, 사업 지원 및 임대 서비스업",
    "공공행정, 국방 및 사회보장 행정",
    "교육 서비스업",
    "보건업 및 사회복지 서비스업",
    "예술, 스포츠 및 여가관련 서비스업",
    "협회 및 단체, 수리 및 기타 개인 서비스업",
    "국제 및 외국기관",
]

# 연도별로 데이터를 합치기
combined_data = []

for year in range(2012, 2024):
    # 해당 연도의 고령 근로자 데이터 필터링
    elder_worker_year = elder_worker[elder_worker["연도"] == year]

    # 서비스업 총 근로자 수와 고령 근로자 수 계산
    service_total = elder_worker_year[
        elder_worker_year["구분"].isin(service_industries)
    ]["전체근로자수"].sum()

    service_elder = elder_worker_year[
        elder_worker_year["구분"].isin(service_industries)
    ]["고령근로자수"].sum()

    # 산업별 매핑 생성
    industry_mapping = {
        "제조업": {
            "전체": elder_worker_year[elder_worker_year["구분"] == "제조업"][
                "전체근로자수"
            ].sum(),
            "고령": elder_worker_year[elder_worker_year["구분"] == "제조업"][
                "고령근로자수"
            ].sum(),
        },
        "건설업": {
            "전체": elder_worker_year[elder_worker_year["구분"] == "건설업"][
                "전체근로자수"
            ].sum(),
            "고령": elder_worker_year[elder_worker_year["구분"] == "건설업"][
                "고령근로자수"
            ].sum(),
        },
        "농업, 임업 및 어업": {
            "전체": elder_worker_year[elder_worker_year["구분"] == "농업 임업 및 어업"][
                "전체근로자수"
            ].sum(),
            "고령": elder_worker_year[elder_worker_year["구분"] == "농업 임업 및 어업"][
                "고령근로자수"
            ].sum(),
        },
        "서비스업": {"전체": service_total, "고령": service_elder},
        "합계": {
            "전체": elder_worker_year[elder_worker_year["구분"] == "소계"][
                "전체근로자수"
            ].sum(),
            "고령": elder_worker_year[elder_worker_year["구분"] == "소계"][
                "고령근로자수"
            ].sum(),
        },
    }

    # 외국인 근로자 데이터 처리
    foreign_worker_year = foreign_worker_by_industries[["업종별", str(year)]].set_index(
        "업종별"
    )
    foreign_worker_year.loc["농업, 임업 및 어업"] = foreign_worker_year.loc[
        ["농축산업", "어업"]
    ].sum()
    foreign_worker_year.drop(["농축산업", "어업"], inplace=True)

    # 데이터프레임 생성
    result_dict = {}
    for industry in industry_mapping.keys():
        result_dict[industry] = {
            "고령근로자수": industry_mapping[industry]["고령"],
            "비고령근로자수": industry_mapping[industry]["전체"]
            - industry_mapping[industry]["고령"],
            "외국인 근로자 수": (
                foreign_worker_year.loc[industry, str(year)]
                if industry in foreign_worker_year.index
                else 0
            ),
        }
        result_dict[industry]["총근로자수"] = (
            result_dict[industry]["고령근로자수"]
            + result_dict[industry]["비고령근로자수"]
            + result_dict[industry]["외국인 근로자 수"]
        )

    year_df = pd.DataFrame.from_dict(result_dict, orient="index")
    year_df["연도"] = year

    # 비중 계산
    for col in ["고령근로자수", "비고령근로자수", "외국인 근로자 수"]:
        year_df[f"{col}_비중"] = (year_df[col] / year_df["총근로자수"] * 100).round(2)

    # 데이터 추가
    combined_data.append(year_df)

# 모든 연도의 데이터를 하나로 합치기
combined_df = pd.concat(combined_data)

# 2012년 대비 2023년 증가율 계산
df_2012 = combined_df[combined_df["연도"] == 2012]
df_2023 = combined_df[combined_df["연도"] == 2023]

growth_rate = pd.DataFrame(
    {
        2012: df_2012["외국인 근로자 수"].values,
        2023: df_2023["외국인 근로자 수"].values,
    },
    index=df_2012.index,
)

growth_rate["증가율(%)"] = ((growth_rate[2023] / growth_rate[2012] - 1) * 100).round(2)

# 결과 출력
print("\n=== 2023년 산업별 근로자 현황 ===")
current_status = combined_df[combined_df["연도"] == 2023].sort_values(
    "외국인 근로자 수_비중", ascending=False
)
print(
    current_status[
        [
            "고령근로자수",
            "고령근로자수_비중",
            "비고령근로자수",
            "비고령근로자수_비중",
            "외국인 근로자 수",
            "외국인 근로자 수_비중",
            "총근로자수",
        ]
    ]
)

print("\n=== 2012년 대비 2023년 외국인 근로자 증가율 ===")
print(growth_rate["증가율(%)"].sort_values(ascending=False))

# 시각화
plt.figure(figsize=(12, 6))
industries = combined_df.index.unique()
for industry in industries:
    if industry != "합계":  # 합계 제외
        industry_data = combined_df[combined_df.index == industry]
        plt.plot(
            industry_data["연도"],
            industry_data["외국인 근로자 수_비중"],
            label=industry,
            marker="o",
        )

plt.title("산업별 외국인 근로자 비중 추이 (2012-2023)")
plt.xlabel("연도")
plt.ylabel("외국인 근로자 비중 (%)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()

# 2023년 산업별 근로자 구성 비율 시각화
current_data = combined_df[combined_df["연도"] == 2023]
current_data = current_data[current_data.index != "합계"]  # 합계 제외

fig, ax = plt.subplots(figsize=(12, 6))
bottom = np.zeros(len(current_data))

for category in ["비고령근로자수_비중", "고령근로자수_비중", "외국인 근로자 수_비중"]:
    plt.bar(current_data.index, current_data[category], bottom=bottom, label=category)
    bottom += current_data[category]

plt.title("2023년 산업별 근로자 구성 비율")
plt.xlabel("산업")
plt.ylabel("비중 (%)")
plt.legend(title="근로자 구분")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
