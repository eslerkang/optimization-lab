import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


# Hyperparameters 설정
SEED = 486
ALPHA_S = 0.05
ALPHA_E = 0.1
BETA = 0.05
K = 0.5

# 재현성을 위한 시드 설정
np.random.seed(SEED)

# Data 불러오기 및 설정
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


# 랜덤하게 Due Time 및 Queue Time 설정
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


# 해당 스테이지마다 활성화되는 Queue Time 업데이트 및 Queue time 타이머 가동
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


# 해당 스테이지에 대해 분배되는 Slack time 계산
def get_slack(lot, stage, time):
    total_remaining_processing_time = sum(
        [processing_times[i] for i in range(stage, 4)]
    )
    # 납기 - 현재 시간 - 남은 작업 시간
    due_slack = lot["due"] - time - total_remaining_processing_time
    active_q_time = lot["active_q_time"]

    # 납기 Slack에 대해 남은 스테이지들의 작업시간에 따른 비율 계산
    current_stage_processing_time = processing_times[stage]
    fraction_of_current_stage_processing_time = (
        current_stage_processing_time / total_remaining_processing_time
    )

    # 현재 스테이지에 할당되는 납기 Slack
    current_stage_due_slack = due_slack * fraction_of_current_stage_processing_time

    # Queue Time 범위 사이에 있는 스테이지에서의 작업 시간
    q_range_remaining_processing_time = (
        sum([processing_times[i] for i in range(stage, active_q_time["end"])])
        if active_q_time is not None
        else 0
    )
    # Queue time이 여러 스테이지에 걸쳐 있을 경우 현재 스테이지에서의 Queue Time 비율 계산
    fraction_of_current_stage_processing_time = 1
    if q_range_remaining_processing_time != 0:
        fraction_of_current_stage_processing_time = (
            q_range_remaining_processing_time
            / (
                q_range_remaining_processing_time
                + processing_times[active_q_time["end"]]
            )
        )
    # Queue Time Slack = Queue Time 납기 - 현재 시간 - Queue Time 범위 사이의 남은 작업 시간
    # Queue time 구간이 없는 상태일 경우 현재 스테이지의 납기 Slack을 그대로 사용
    q_slack = (
        active_q_time["due"] - time - q_range_remaining_processing_time
        if active_q_time is not None
        else current_stage_due_slack
    )
    # 현재 스테이지에 할당되는 Queue Time Slack
    current_stage_q_slack = q_slack * fraction_of_current_stage_processing_time

    return current_stage_due_slack, current_stage_q_slack


# 휴리스틱 알고리즘을 통한 Priority score 계산
def calculate_score(lot, stage, time):
    due_slack, q_slack = get_slack(lot, stage, time)

    return np.exp(-K * due_slack) * np.exp(-(1 - K) * max(0, q_slack))


generate_due()
generate_queue_time()


# 메인 시뮬레이션
for stage in range(4):
    # 현재 스테이지로 들어온 작업들 중 가장 빨리 들어온 작업의 시간을 기준으로 시뮬레이션 진행
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


def plot_result():
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

    df = pd.DataFrame(results)

    base_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    df["Start"] = df["Start"].apply(lambda x: base_date + datetime.timedelta(minutes=x))
    df["End"] = df["End"].apply(lambda x: base_date + datetime.timedelta(minutes=x))

    lot_due = {lot["name"]: lot["due"] for lot in lot_data}

    lot_qtime_violation = {}
    lot_tardiness = {}
    lot_details = []

    for lot in lot_data:
        lot_id = lot["name"]
        due_time = lot_due[lot_id]
        end_time = df[df["Lot"] == lot_id]["End"].max()
        start_time = df[df["Lot"] == lot_id]["Start"].min()
        tardiness = (
            end_time - (base_date + datetime.timedelta(minutes=due_time))
        ).total_seconds() / 60
        tardiness = max(0, tardiness)

        qtime_info = []
        qtime_violations = []
        for qtime in lot["qtime"]:
            q_start_stage = qtime["start"]
            q_end_stage = qtime["end"]
            q_due_time = qtime["due"]

            q_start_time = df[
                (df["Lot"] == lot_id) & (df["Stage"] == q_start_stage + 1)
            ]["End"].max()
            q_end_time = df[(df["Lot"] == lot_id) & (df["Stage"] == q_end_stage + 1)][
                "Start"
            ].min()

            if (
                pd.notna(q_start_time)
                and pd.notna(q_end_time)
                and (q_end_time - base_date).total_seconds() / 60 > q_due_time
            ):
                qtime_violations.append(True)
            else:
                qtime_violations.append(False)

            qtime_info.append(
                {
                    "Q-Time Start Time": (
                        (q_start_time - base_date).total_seconds() / 60
                        if pd.notna(q_start_time)
                        else None
                    ),
                    "Q-Time End Time": (
                        (q_end_time - base_date).total_seconds() / 60
                        if pd.notna(q_end_time)
                        else None
                    ),
                    "Q-Time Due": q_due_time,
                    "Violated": (
                        (q_end_time - base_date).total_seconds() / 60 > q_due_time
                        if pd.notna(q_end_time)
                        else False
                    ),
                }
            )

        lot_qtime_violation[lot_id] = any(qtime_violations)
        lot_tardiness[lot_id] = tardiness

        lot_details.append(
            {
                "Lot": lot_id,
                "Start": (start_time - base_date).total_seconds() / 60,
                "End": (end_time - base_date).total_seconds() / 60,
                "Due": due_time,
                "Tardiness": tardiness,
                "Q-Time Violations": qtime_info,
            }
        )

    df["Q-Time Violation"] = df["Lot"].map(lot_qtime_violation)
    df["Tardiness"] = df["Lot"].map(lot_tardiness)
    df["Due"] = df["Lot"].map(lot_due)

    df = df.sort_values(by="Lot")

    fig_gantt = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Machine",
        color="Lot",
        text="Lot",
        hover_data={"Q-Time Violation": True, "Tardiness": True, "Due": True},
    )
    fig_gantt.update_yaxes(categoryorder="category ascending")
    fig_gantt.update_layout(
        title="Gantt Chart",
        xaxis_title="Time",
        yaxis_title="Machines",
        legend_title="Lots",
        font=dict(size=12),
        showlegend=True,
    )

    lot_info = []
    for detail in lot_details:
        qtime_str = "<br>".join(
            [
                f"Start: {q['Q-Time Start Time']}<br>End: {q['Q-Time End Time']}<br>Due: {q['Q-Time Due']}<br>Violated: {q['Violated']}"
                for q in detail["Q-Time Violations"]
            ]
        )
        lot_info.append(
            {
                "Lot": detail["Lot"],
                "Start": detail["Start"],
                "End": detail["End"],
                "Due": detail["Due"],
                "Tardiness": detail["Tardiness"],
                "Q-Time Info": qtime_str,
            }
        )

    lot_info_df = pd.DataFrame(lot_info)

    fig_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["Lot", "Start", "End", "Due", "Tardiness", "Q-Time Info"],
                    fill_color="paleturquoise",
                    align="left",
                ),
                cells=dict(
                    values=[lot_info_df[k].apply(str) for k in lot_info_df.columns],
                    fill_color="lavender",
                    align="left",
                ),
            )
        ]
    )

    late_lots_count = sum(l > 0 for l in lot_tardiness.values())
    qtime_violations_count = sum(lot_qtime_violation.values())

    # Dash 애플리케이션 설정
    app = Dash(__name__)

    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
    )

    # 각 페이지 레이아웃
    index_page = html.Div(
        [
            html.H1("Gantt Chart and Lot Information"),
            dcc.Link("Go to Gantt Chart", href="/gantt-chart"),
            html.Br(),
            dcc.Link("Go to Lot Information Table", href="/lot-info"),
        ]
    )

    gantt_chart_page = html.Div(
        [
            html.H1("Gantt Chart"),
            dcc.Graph(figure=fig_gantt),
            html.Br(),
            dcc.Link("Go to Lot Information Table", href="/lot-info"),
            html.Br(),
            dcc.Link("Go back to home", href="/"),
        ]
    )

    lot_info_page = html.Div(
        [
            html.H1("Lot Information Table"),
            dcc.Graph(figure=fig_table),
            html.Br(),
            html.Div(f"Number of late lots: {late_lots_count}"),
            html.Div(f"Number of q-time violations: {qtime_violations_count}"),
            html.Br(),
            dcc.Link("Go to Gantt Chart", href="/gantt-chart"),
            html.Br(),
            dcc.Link("Go back to home", href="/"),
        ]
    )

    # 페이지 전환 콜백
    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/gantt-chart":
            return gantt_chart_page
        elif pathname == "/lot-info":
            return lot_info_page
        else:
            return index_page

    if __name__ == "__main__":
        app.run_server(debug=True)


plot_result()
