import pandas as pd

ALPHA_S = 0.2
ALPHA_E = 0.5
BETA = 0.05

K = 0.5

lot_data = pd.read_csv("./lot_data.csv").to_dict("records")
machine_num = [3, 2, 3, 2]
processing_times = [45, 60, 120, 60]
q_time = [
    {"type": 1, "start": 1, "end": 2},
    {"type": 1, "start": 2, "end": 3},
    {"type": 2, "start": 1, "end": 3},
    {"type": 3, "start": 3, "end": 4},
]
