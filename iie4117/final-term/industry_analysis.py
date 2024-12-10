"""
산업별 현황 분석 (Industry Analysis)

이 파일은 2023년 기준 산업별 고령화 현황을 분석합니다.
주요 분석 내용:
1. 산업별 고령화율 현황
2. 산업별 성별 분포
3. 외국인 근로자 현황 및 산업 연계성
"""

import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"

# 1. 데이터 로드 및 전처리
elder_worker = pd.read_csv("datas/elder_worker.csv")
foreign_worker = pd.read_csv("datas/foreign_worker_by_year.csv")

# 2023년 데이터 추출
elder_2023 = elder_worker[elder_worker["연도"] == 2023].copy()
elder_2023 = elder_2023[elder_2023["구분"] != "소계"]

# 컬럼명 변경
elder_2023 = elder_2023.rename(
    columns={
        "구분": "산업",
        "전체근로자수": "전체근로자",
        "고령근로자수": "55세이상근로자",
        "고령남성근로자수": "55세이상남성",
        "고령여성근로자수": "55세이상여성",
    }
)

# 2. 산업별 지표 계산
elder_2023["고령화율"] = (elder_2023["55세이상근로자"] / elder_2023["전체근로자"]) * 100
elder_2023["성별격차"] = (
    (elder_2023["55세이상남성"] - elder_2023["55세이상여성"])
    / elder_2023["55세이상근로자"]
    * 100
)
elder_2023["산업규모"] = elder_2023["전체근로자"] / elder_2023["전체근로자"].sum() * 100

# 산업명 축약
elder_2023["산업_축약"] = elder_2023["산업"].apply(
    lambda x: x[:15] + "..." if len(x) > 15 else x
)

# 3. 시각화: 산업별 현황 매트릭스
plt.figure(figsize=(15, 8))
plt.scatter(
    elder_2023["고령화율"],
    elder_2023["산업규모"],
    s=abs(elder_2023["성별격차"]) * 50,
    alpha=0.6,
)

# 산업명 레이블 추가
for idx, row in elder_2023.iterrows():
    plt.annotate(
        row["산업_축약"],
        (row["고령화율"], row["산업규모"]),
        xytext=(5, 5),
        textcoords="offset points",
    )

plt.title("산업별 고령화 현황 매트릭스 (2023년)")
plt.xlabel("고령화율 (%)")
plt.ylabel("산업규모 (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. 외국인 근로자 현황
current_foreign = float(foreign_worker[foreign_worker["year"] == 2023]["total"]) * 10000
total_workers = elder_2023["전체근로자"].sum()
foreign_ratio = current_foreign / total_workers * 100

# 외국인 근로자 추이 시각화
plt.figure(figsize=(12, 6))

# 연도별 외국인 근로자 수 추출 (만명 단위를 명 단위로 변환)
years = foreign_worker["year"].astype(str)
workers = foreign_worker["total"].astype(float) * 10000

# 선 그래프 그리기
plt.plot(years, workers, marker="o", linewidth=2, markersize=8)

# 각 포인트에 값 표시
for i, v in enumerate(workers):
    plt.text(i, v + 10000, f"{v:,.0f}명", ha="center", va="bottom")

plt.title("연도별 외국인 근로자 현황")
plt.xlabel("연도")
plt.ylabel("외국인 근로자 수 (명)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. 분석 결과 출력
print("\n=== 산업별 고령화 현황 분석 (2023년) ===")

# 고령화율 기준 상위 5개 산업
print("\n1. 고령화율 상위 5개 산업")
top_5_aging = elder_2023.nlargest(5, "고령화율")
for _, row in top_5_aging.iterrows():
    print(f"\n{row['산업']}:")
    print(f"- 고령화율: {row['고령화율']:.1f}%")
    print(f"- 전체 근로자: {row['전체근로자']:,.0f}명")
    print(
        f"- 성별 분포: 남성 {row['55세이상남성']:,.0f}명, 여성 {row['55세이상여성']:,.0f}명"
    )
    print(f"- 산업규모: {row['산업규모']:.1f}%")

# 산업규모 기준 상위 5개 산업의 고령화 현황
print("\n2. 주요 산업(규모 기준 상위 5개)의 고령화 현황")
top_5_size = elder_2023.nlargest(5, "산업규모")
for _, row in top_5_size.iterrows():
    print(f"\n{row['산업']}:")
    print(f"- 산업규모: {row['산업규모']:.1f}%")
    print(f"- 고령화율: {row['고령화율']:.1f}%")
    print(f"- 성별격차: {row['성별격차']:.1f}%")

print(f"\n3. 외국인 근로자 현황")
print(f"- 전체 외국인 근로자 수: {current_foreign:,.0f}명")
print(f"- 전체 근로자 대비 비율: {foreign_ratio:.1f}%")
print(
    f"- 전년 대비 증감률: {float(foreign_worker[foreign_worker['year'] == 2023]['change'].iloc[0]):.1f}%"
)
