# 필요한 라이브러리 불러오기
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# 이동 시간 매트릭스 로드
duration_df = pd.read_csv("./tour_distances_matrix.csv", index_col=0)
stay_df = pd.read_csv("./residence_time.csv", index_col=0)
stay_time = stay_df["Avg_Stay_Duration"].values

total_day = 7

# 위치 정보 로드
geo_df = pd.read_csv("./geo_info.csv")
geo_df["Cluster"] = (
    KMeans(n_clusters=total_day, random_state=42)
    .fit(geo_df[["Latitude", "Longitude"]])
    .labels_
)

# 숙소 정보
base_location = "Bukchon Hanok Village"

# 각 클러스터별 TSP 문제 해결 및 출력
for day in range(total_day):
    # 현재 클러스터의 관광지 선택
    cluster_locations = [base_location] + geo_df[geo_df["Cluster"] == day][
        "Name"
    ].tolist()
    # 이동 시간 매트릭스 추출
    cluster_matrix = duration_df.loc[cluster_locations, cluster_locations].to_numpy()

    # TSP 문제 설정 및 해결
    manager = pywrapcp.RoutingIndexManager(len(cluster_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(
        lambda from_index, to_index: cluster_matrix[manager.IndexToNode(from_index)][
            manager.IndexToNode(to_index)
        ]
        + stay_time[to_index]
    )
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    solution = routing.SolveWithParameters(search_parameters)
    # 결과 출력
    total_seconds = solution.ObjectiveValue()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    print(f"Day {day+1} Tour Order(with {hours} hours {minutes} minutes):")
    index = routing.Start(0)
    while not routing.IsEnd(index):
        print(f"{cluster_locations[manager.IndexToNode(index)]} -> ", end="")
        index = solution.Value(routing.NextVar(index))
    print(base_location)
    print()
