import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

data = pd.read_csv("data.csv")

group1_data = data[data["group"] == 1]
group2_data = data[data["group"] == 2]

kmf_1 = KaplanMeierFitter()
kmf_1.fit(
    durations=group1_data["time"], event_observed=group1_data["event"], label="Group 1"
)

kmf_2 = KaplanMeierFitter()
kmf_2.fit(
    durations=group2_data["time"], event_observed=group2_data["event"], label="Group 2"
)

kmf_1.plot()
kmf_2.plot()
plt.grid(True)
plt.show()

results = logrank_test(
    durations_A=group1_data["time"],
    durations_B=group2_data["time"],
    event_observed_A=group1_data["event"],
    event_observed_B=group2_data["event"],
)

results.print_summary()
