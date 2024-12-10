import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"

# 데이터 로드
elder_worker = pd.read_csv("datas/elder_worker.csv")
foreign_worker = pd.read_csv("datas/foreign_worker_by_year.csv")

# 2023년 산업별 데이터 추출
elder_2023 = elder_worker[elder_worker["연도"] == 2023].copy()
elder_2023 = elder_2023[elder_2023["구분"] != "소계"]

# 데이터 전처리
elder_2023 = elder_2023.rename(
    columns={
        "구분": "산업",
        "전체근로자수": "전체근로자",
        "고령근로자수": "55세이상근로자",
        "고령남성근로자수": "55세이상남성",
        "고령여성근로자수": "55세이상여성",
    }
)

numeric_cols = ["전체근로자", "55세이상근로자", "55세이상남성", "55세이상여성"]
for col in numeric_cols:
    elder_2023[col] = pd.to_numeric(elder_2023[col], errors="coerce")

# 개선된 인력수급위험도 계산
elder_2023["고령화율"] = elder_2023["55세이상근로자"] / elder_2023["전체근로자"] * 100
elder_2023["성비불균형"] = (
    abs(elder_2023["55세이상남성"] - elder_2023["55세이상여성"])
    / elder_2023["55세이상근로자"]
    * 100
)
elder_2023["규모대비고령화"] = (
    elder_2023["55세이상근로자"] / elder_2023["55세이상근로자"].mean() * 100
)

# 인력수급위험도 계산
elder_2023["인력수급위험도"] = (
    elder_2023["고령화율"] * 0.4
    + elder_2023["성비불균형"] * 0.3
    + elder_2023["규모대비고령화"] * 0.3
)

# 시각화
plt.figure(figsize=(15, 8))
risk_data = elder_2023.nlargest(10, "인력수급위험도")[
    ["산업", "고령화율", "성비불균형", "규모대비고령화"]
]

# 스택 바 차트로 각 요소별 기여도 표시
bottom = np.zeros(10)
for column, weight in [("고령화율", 0.4), ("성비불균형", 0.3), ("규모대비고령화", 0.3)]:
    plt.bar(risk_data["산업"], risk_data[column] * weight, bottom=bottom, label=column)
    bottom += risk_data[column] * weight

plt.title("산업별 인력수급 위험도 구성요소 (상위 10개 산업)")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()

# 2. 위험도와 외국인 근로자 비율 관계
total_workers = elder_2023["전체근로자"].sum()
foreign_workers_2023 = (
    float(foreign_worker[foreign_worker["year"] == 2023]["total"]) * 10000
)
foreign_ratio = foreign_workers_2023 / total_workers * 100

# 3. 분석 결과 출력
print("\n=== 산업별 인력 수급 위험도 상세 분석 ===")
high_risk = elder_2023.nlargest(5, "인력수급위험도")
for _, row in high_risk.iterrows():
    print(f"\n{row['산업']}:")
    print(f"- 총 위험도: {row['인력수급위험도']:.1f}")
    print(
        f"  * 고령화율 기여도: {row['고령화율']*0.4:.1f} (고령화율: {row['고령화율']:.1f}%)"
    )
    print(
        f"  * 성비불균형 기여도: {row['성비불균형']*0.3:.1f} (불균형율: {row['성비불균형']:.1f}%)"
    )
    print(
        f"  * 규모대비 기여도: {row['규모대비고령화']*0.3:.1f} (상대규모: {row['규모대비고령화']:.1f}%)"
    )
    print(f"- 전체 근로자: {row['전체근로자']:,.0f}명")
    print(
        f"- 55세 이상: {row['55세이상근로자']:,.0f}명 (남성: {row['55세이상남성']:,.0f}명, 여성: {row['55세이상여성']:,.0f}명)"
    )

print(f"\n전체 산업 외국인 근로자 비율 (2023): {foreign_ratio:.1f}%")
