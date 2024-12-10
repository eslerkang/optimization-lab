import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    oecd_data = pd.read_csv("oecd data.csv")
    population_forecast = pd.read_csv("korea population forecast.csv")
    hospital_use_rate = pd.read_csv("korea hospital use rate.csv")
    return oecd_data, population_forecast, hospital_use_rate


def calculate_oecd_average_doctor_ratio(oecd_data):
    oecd_data["doctor_ratio"] = oecd_data["doctors_count"] / oecd_data["population"]
    latest_year = oecd_data["year"].max()
    latest_data = oecd_data[oecd_data["year"] == latest_year]
    return latest_data["doctor_ratio"].mean()


def predict_future_doctor_demand(
    population_forecast, hospital_use_rate, oecd_average_ratio
):
    latest_year = hospital_use_rate["year"].max()
    latest_use_rate = hospital_use_rate[hospital_use_rate["year"] == latest_year]

    male_use_rate = (
        latest_use_rate[
            (latest_use_rate["category"] == "성별")
            & (latest_use_rate["subcategory"] == "남성")
        ]["outpatient"].values[0]
        + latest_use_rate[
            (latest_use_rate["category"] == "성별")
            & (latest_use_rate["subcategory"] == "남성")
        ]["inpatient"].values[0]
    )
    female_use_rate = (
        latest_use_rate[
            (latest_use_rate["category"] == "성별")
            & (latest_use_rate["subcategory"] == "여성")
        ]["outpatient"].values[0]
        + latest_use_rate[
            (latest_use_rate["category"] == "성별")
            & (latest_use_rate["subcategory"] == "여성")
        ]["inpatient"].values[0]
    )

    future_demand = {}
    for year in population_forecast["year"].unique():
        year_data = population_forecast[population_forecast["year"] == year]
        male_pop = year_data[
            (year_data["category"] == "성별") & (year_data["subcategory"] == "남성")
        ]["population"].values[0]
        female_pop = year_data[
            (year_data["category"] == "성별") & (year_data["subcategory"] == "여성")
        ]["population"].values[0]

        weighted_population = (
            male_pop * male_use_rate + female_pop * female_use_rate
        ) / 100
        future_demand[year] = weighted_population * oecd_average_ratio

    return pd.Series(future_demand)


def predict_future_doctors_and_graduates(
    oecd_data, population_forecast, retirement_rate
):
    korea_data = oecd_data[oecd_data["country_code"] == "KOR"].sort_values("year")

    current_year = korea_data["year"].max()
    current_doctors = korea_data[korea_data["year"] == current_year][
        "doctors_count"
    ].values[0]
    current_graduates = korea_data["graduates_count"].tail(6).mean()

    forecast_years = population_forecast["year"].unique()

    future_doctors = []
    future_graduates = []

    for i in range(len(forecast_years)):
        if i == 0:
            doctors = current_doctors
        else:
            doctors = future_doctors[-1]

        retired_doctors = int(doctors * retirement_rate)
        new_doctors = int(current_graduates)
        doctors = doctors - retired_doctors + new_doctors

        future_doctors.append(doctors)
        future_graduates.append(new_doctors)

    return pd.DataFrame(
        {
            "year": forecast_years,
            "predicted_doctors": future_doctors,
            "predicted_graduates": future_graduates,
        }
    )


def calculate_required_increase(combined_data, education_years=6, tolerance_ratio=0.05):
    required_increase = []
    for i, row in combined_data.iterrows():
        if i < education_years:
            required_increase.append(0)
            continue

        current_demand = row["predicted_demand"]
        future_doctors = (
            combined_data.iloc[i]["new_predicted_doctors"]
            if i < len(combined_data) - education_years
            else combined_data.iloc[-1]["new_predicted_doctors"]
        )

        ongoing_increase = sum(required_increase[max(0, i - education_years) : i])
        future_doctors += ongoing_increase

        shortage = current_demand - future_doctors

        if abs(shortage) / current_demand <= tolerance_ratio:
            required_increase.append(0)
        else:
            required_increase.append(max(0, int(shortage / education_years)))

    return required_increase


# 데이터 로드 및 예측 실행
oecd_data, population_forecast, hospital_use_rate = load_data()
oecd_average_ratio = calculate_oecd_average_doctor_ratio(oecd_data)

first_year = population_forecast["year"].unique()[0]
year_data = population_forecast[population_forecast["year"] == first_year]
total_population = year_data[year_data["category"] == "성별"]["population"].sum()
over_60_population = year_data[
    (year_data["category"] == "연령") & (year_data["subcategory"] == "60세 이상")
]["population"].values[0]
retirement_rate = (over_60_population / total_population) / 5

future_demand = predict_future_doctor_demand(
    population_forecast, hospital_use_rate, oecd_average_ratio
)
future_doctors_and_graduates = predict_future_doctors_and_graduates(
    oecd_data, population_forecast, retirement_rate
)

# 데이터 병합 및 증원량 계산
future_demand_df = pd.DataFrame(
    {"year": future_demand.index, "predicted_demand": future_demand.values}
)
combined_data = pd.merge(future_doctors_and_graduates, future_demand_df, on="year")

# 새로운 의사 수와 졸업생 수 계산을 위한 반복문
new_graduates = combined_data["predicted_graduates"].tolist()
new_doctors = [combined_data.iloc[0]["predicted_doctors"]]

for i in range(1, len(combined_data)):
    current_doctors = new_doctors[-1]
    retired_doctors = int(current_doctors * retirement_rate)
    new_doctor_graduates = new_graduates[i]
    doctors = current_doctors - retired_doctors + new_doctor_graduates
    new_doctors.append(doctors)

combined_data["new_predicted_doctors"] = new_doctors
combined_data["new_graduates"] = new_graduates

required_increase = calculate_required_increase(combined_data)
combined_data["required_increase"] = required_increase

# 증원을 반영한 새로운 졸업생 수와 의사 수 계산
for i in range(6, len(combined_data)):
    combined_data.loc[i, "new_graduates"] += combined_data.loc[
        i - 6, "required_increase"
    ]

new_doctors = [combined_data.iloc[0]["predicted_doctors"]]
for i in range(1, len(combined_data)):
    current_doctors = new_doctors[-1]
    retired_doctors = int(current_doctors * retirement_rate)
    new_doctor_graduates = combined_data.loc[i, "new_graduates"]
    doctors = current_doctors - retired_doctors + new_doctor_graduates
    new_doctors.append(doctors)

combined_data["new_predicted_doctors"] = new_doctors

print("Predicted future doctors, graduates, demand, and required increase:")
print(combined_data)
combined_data.to_csv("combined.csv", index=False)

print(f"Retirement rate: {retirement_rate:.4f}")
print(f"Initial number of doctors: {combined_data.iloc[0]['predicted_doctors']}")
print(f"Initial number of graduates: {combined_data.iloc[0]['predicted_graduates']}")
print(
    f"Final number of doctors (without increase): {combined_data.iloc[-1]['predicted_doctors']}"
)
print(
    f"Final number of doctors (with increase): {combined_data.iloc[-1]['new_predicted_doctors']}"
)
print(
    f"Final number of graduates (with increase): {combined_data.iloc[-1]['new_graduates']}"
)
print(f"Final demand: {combined_data.iloc[-1]['predicted_demand']}")

plt.figure(figsize=(16, 10))  # 그래프 크기를 더 크게 조정

plt.plot(
    combined_data["year"],
    combined_data["predicted_doctors"],
    label="Predicted Doctors (Original)",
    color="blue",
    linestyle="--",
)
plt.plot(
    combined_data["year"],
    combined_data["new_predicted_doctors"],
    label="Predicted Doctors (With Increase)",
    color="darkblue",
)
plt.plot(
    combined_data["year"],
    combined_data["predicted_demand"],
    label="Predicted Demand",
    color="red",
)

plt.title("Predicted Doctors, Demand, and Graduates in Korea", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Doctors", fontsize=12)
plt.grid(True, alpha=0.3)

plt.ylim(
    0,
    max(
        combined_data["predicted_demand"].max(),
        combined_data["new_predicted_doctors"].max(),
    )
    * 1.1,
)

ax2 = plt.twinx()
ax2.plot(
    combined_data["year"],
    combined_data["predicted_graduates"],
    label="Current Graduates",
    color="limegreen",
    linestyle="--",
)
ax2.plot(
    combined_data["year"],
    combined_data["new_graduates"],
    label="New Graduates",
    color="darkgreen",
)
ax2.set_ylabel("Annual Number of Graduates", color="darkgreen", fontsize=12)
ax2.tick_params(axis="y", labelcolor="darkgreen")

# 범례 위치 조정
lines1, labels1 = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    fancybox=True,
    shadow=True,
    fontsize=10,
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)  # 그래프 아래쪽 여백 추가
plt.show()
