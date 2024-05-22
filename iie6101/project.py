import numpy as np
import pandas as pd

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
    for lot in lot_data:
        lot["qtime"] = []
        q_info = list(filter(lambda x: x["type"] == lot["type"], q_time))
        for q in q_info:
            total_processing_time_in_q_time_range = 0
            for i in range(q["start"], q["end"]):
                total_processing_time_in_q_time_range += processing_times[i + 1]
            lot["qtime"].append(
                {
                    "start": q["start"],
                    "end": q["end"],
                    "qtime": total_processing_time_in_q_time_range
                    + np.rint(
                        np.random.uniform(
                            0, BETA * total_processing_time_in_q_time_range
                        )
                    ),
                }
            )

    print(lot_data)


def update_slack(lot, stage, time):
    due_slack = lot["due"] - time - sum([processing_times[i] for i in range(stage, 4)])
    activated_q_time = None
    if filter(lambda x: x["start"] + 1 <= stage and x["end"] >= stage, lot["qtime"]):
        activated_q_time = list(
            filter(
                lambda x: x["start"] + 1 <= stage and x["end"] >= stage, lot["qtime"]
            )
        )[0]


generate_due()
generate_queue_time()

# Main algorithm

for stage in range(4):
    TIME = np.min([lot["release"] for lot in lot_data])
    machines_in_stage = machines[stage]
    lots_to_process = lot_data.copy()
    while True:
        for busy_machine in filter(lambda x: x["busy"], machines_in_stage):
            if busy_machine["history"][-1]["end"] == TIME:
                busy_machine["busy"] = False
        machine_lot_score = []
        if lots_to_process:
            for machine in filter(lambda x: not x["busy"], machines_in_stage):
                for lot in lots_to_process:
                    if lot["release"] <= TIME:
                        lot = update_slack(lot, stage, TIME)
