import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.express as px

# Hyperparameters
SEED = 486
ALPHA_S = 0.05
ALPHA_E = 0.1
BETA = 0.05
K = 0.5

np.random.seed(SEED)

# Data
lot_data = pd.read_csv("./lot_data.csv").to_dict("records")
processing_times = [45, 60, 120, 60]
q_time = [
    {"type": 1, "start": 0, "end": 1},
    {"type": 1, "start": 1, "end": 2},
    {"type": 2, "start": 0, "end": 2},
    {"type": 3, "start": 2, "end": 3},
]
machines = [
    [
        {"id": 1, "history": [], "busy": False},
        {"id": 2, "history": [], "busy": False},
        {"id": 3, "history": [], "busy": False},
    ],
    [
        {"id": 1, "history": [], "busy": False},
        {"id": 2, "history": [], "busy": False},
    ],
    [
        {"id": 1, "history": [], "busy": False},
        {"id": 2, "history": [], "busy": False},
        {"id": 3, "history": [], "busy": False},
    ],
    [
        {"id": 1, "history": [], "busy": False},
        {"id": 2, "history": [], "busy": False},
    ],
]


# Utils
def generate_due():
    total_processing_time = sum(processing_times)
    for lot in lot_data:
        lot["due"] = total_processing_time + np.rint(
            np.random.uniform(
                ALPHA_S * total_processing_time, ALPHA_E * total_processing_time
            )
        )


def generate_queue_time():
    for q in q_time:
        total_processing_time_in_q_time_range = 0
        for i in range(q["start"], q["end"]):
            total_processing_time_in_q_time_range += processing_times[i + 1]
        q["limit"] = total_processing_time_in_q_time_range + np.rint(
            np.random.uniform(0, BETA * total_processing_time_in_q_time_range)
        )

    for lot in lot_data:
        lot["qtime"] = []
        lot_type = lot["type"]
        q_info = list(filter(lambda x: x["type"] == lot_type, q_time))
        for q in q_info:
            lot["qtime"].append(
                {
                    "start": q["start"],
                    "end": q["end"],
                    "limit": q["limit"],
                }
            )


def update_queue_time_state(lot, stage):
    active_q_time = list(
        filter(lambda x: x["start"] + 1 <= stage and x["end"] >= stage, lot["qtime"])
    )
    active_q_time = active_q_time[0] if active_q_time else None
    if active_q_time is not None:
        if active_q_time["start"] + 1 == stage:
            active_q_time["start_time"] = lot["release"]
            active_q_time["due"] = active_q_time["start_time"] + active_q_time["limit"]
    lot["active_q_time"] = active_q_time


def get_slack(lot, stage, time):
    total_remaining_processing_time = sum(
        [processing_times[i] for i in range(stage, 4)]
    )
    due_slack = lot["due"] - time - total_remaining_processing_time
    active_q_time = lot["active_q_time"]

    current_stage_processing_time = processing_times[stage]
    fraction_of_current_stage_processing_time = (
        current_stage_processing_time / total_remaining_processing_time
    )

    current_stage_due_slack = due_slack * fraction_of_current_stage_processing_time

    q_range_remaining_processing_time = (
        sum([processing_times[i] for i in range(stage, active_q_time["end"])])
        if active_q_time is not None
        else 0
    )
    fraction_of_current_stage_processing_time = 1
    if q_range_remaining_processing_time != 0:
        fraction_of_current_stage_processing_time = (
            q_range_remaining_processing_time
            / (
                q_range_remaining_processing_time
                + processing_times[active_q_time["end"]]
            )
        )
    q_slack = (
        active_q_time["due"] - time - q_range_remaining_processing_time
        if active_q_time is not None
        else current_stage_due_slack
    )
    current_stage_q_slack = q_slack * fraction_of_current_stage_processing_time

    return current_stage_due_slack, current_stage_q_slack


def calculate_score(lot, stage, time):
    due_slack, q_slack = get_slack(lot, stage, time)

    return np.exp(-K * due_slack) * np.exp(-(1 - K) * max(0, q_slack))


generate_due()
generate_queue_time()


# Main algorithm
for stage in range(4):
    TIME = np.min([lot["release"] for lot in lot_data])
    machines_in_stage = machines[stage]
    lots_to_process = lot_data.copy()
    for lot in lots_to_process:
        update_queue_time_state(lot, stage)
    while True:
        for busy_machine in filter(lambda x: x["busy"], machines_in_stage):
            if busy_machine["history"][-1]["end"] == TIME:
                busy_machine["history"][-1]["lot"]["release"] = TIME
                busy_machine["busy"] = False
        if lots_to_process:
            for machine in filter(lambda x: not x["busy"], machines_in_stage):
                lot_scores = []
                q_safe_lots = list(
                    filter(
                        lambda x: x["active_q_time"] is None
                        or x["active_q_time"]["due"] >= TIME,
                        lots_to_process,
                    )
                )
                if q_safe_lots:
                    for lot_index, lot in enumerate(lots_to_process):
                        if lot["release"] <= TIME and (
                            lot["active_q_time"] is None
                            or lot["active_q_time"]["due"] >= TIME
                        ):
                            score = calculate_score(lot, stage, TIME)
                            lot_scores.append([lot_index, lot, score])
                else:
                    for lot_index, lot in enumerate(lots_to_process):
                        if lot["release"] <= TIME:
                            score = calculate_score(lot, stage, TIME)
                            lot_scores.append([lot_index, lot, score])
                sorted_lot_scores = sorted(lot_scores, key=lambda x: x[2], reverse=True)
                if sorted_lot_scores:
                    selected_lot = sorted_lot_scores[0][1]
                    selected_lot_index = sorted_lot_scores[0][0]
                    machine["busy"] = True
                    machine["history"].append(
                        {
                            "lot": selected_lot,
                            "start": TIME,
                            "end": TIME + processing_times[stage],
                        }
                    )
                    if selected_lot["active_q_time"] is not None:
                        selected_lot["active_q_time"]["end_time"] = TIME
                    del lots_to_process[selected_lot_index]
        elif not any([machine["busy"] for machine in machines_in_stage]):
            break
        TIME += 1

for lot in lot_data:
    print(lot)

results = []

for stage, machine_list in enumerate(machines):
    for machine in machine_list:
        for history in machine["history"]:
            results.append(
                {
                    "Stage": stage + 1,
                    "Machine": f"Stage {stage + 1} - Machine {machine['id']}",
                    "Lot": history["lot"]["name"],
                    "Start": history["start"],
                    "End": history["end"],
                    "Duration": history["end"] - history["start"],
                }
            )

# Convert results to DataFrame
df = pd.DataFrame(results)

# Convert 'Start' and 'End' to datetime
base_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
df["Start"] = df["Start"].apply(lambda x: base_date + datetime.timedelta(minutes=x))
df["End"] = df["End"].apply(lambda x: base_date + datetime.timedelta(minutes=x))

# Create Gantt chart using Plotly
fig = px.timeline(
    df, x_start="Start", x_end="End", y="Machine", color="Lot", text="Lot"
)
fig.update_yaxes(categoryorder="category ascending")
fig.update_layout(
    title="Gantt Chart",
    xaxis_title="Time",
    yaxis_title="Machines",
    legend_title="Lots",
    font=dict(size=12),
    showlegend=True,
)

# Show the figure
fig.show()
