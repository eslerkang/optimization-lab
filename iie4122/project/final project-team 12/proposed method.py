import random
import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# CSV 파일 경로 설정
DISTANCE_PATH = "./tour_distances_matrix.csv"
DURATION_PATH = "./residence_time.csv"

# CSV 파일 로드
distance_matrix_df = pd.read_csv(DISTANCE_PATH, index_col=0)
duration_matrix_df = pd.read_csv(DURATION_PATH, index_col=0)


moving_time_matrix = distance_matrix_df.values
duration_time_list = duration_matrix_df["Avg_Stay_Duration"].values
travel_point_name = distance_matrix_df.columns.to_list()


random.seed(64)
algorithms.random.seed(64)

total_day = 7

# 유전 알고리즘 설정
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()


# 각 관광지를 무작위 군집에 할당하는 함수
def create_individual():
    return [
        random.randint(0, total_day - 1) for _ in range(len(moving_time_matrix) - 1)
    ]


toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# OR-Tools를 사용하여 군집 내 관광지 순회 시간 계산
def calculate_cluster_time(cluster):
    # 숙소(인덱스 0)를 시작점과 종료점으로 추가
    cluster_with_base = [0] + cluster + [0]

    if len(cluster_with_base) <= 2:
        return 0  # 군집 내 관광지가 없으면 이동 시간은 0

    manager = pywrapcp.RoutingIndexManager(len(cluster_with_base), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    # 거리 콜백 정의
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return (
            moving_time_matrix[cluster_with_base[from_node], cluster_with_base[to_node]]
            + duration_time_list[cluster_with_base[to_node]]
        )

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    )

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        # 순회 시간 계산
        return solution.ObjectiveValue()
    else:
        return 0


# 평가 함수
def evalTour(individual):
    # 군집별로 관광지 인덱스를 분류
    clusters = [[] for _ in range(total_day)]
    for idx, cluster_id in enumerate(individual):
        clusters[cluster_id].append(idx + 1)  # 관광지 인덱스는 1부터 시작
    # 각 군집의 순회 시간 계산
    times = [
        calculate_cluster_time(cluster) for cluster in clusters
    ]  # 숙소 포함하여 계산
    total_travel_time = np.sum(times)
    # 순회 시간의 표준 편차 반환
    if len(times) > 1:
        travel_time_std = np.std(times)
    else:
        travel_time_std = 0  # 단일 군집의 경우 표준 편차는 0

    alpha = 0.4
    fitness = alpha * total_travel_time + (1 - alpha) * travel_time_std

    return (fitness,)


toolbox.register("evaluate", evalTour)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# 유전 알고리즘 실행
population_size = 100
num_generations = 100

pop = toolbox.population(n=population_size)
hof = tools.HallOfFame(1, similar=np.array_equal)

result = algorithms.eaSimple(
    pop,
    toolbox,
    cxpb=0.7,
    mutpb=0.2,
    ngen=num_generations,
    halloffame=hof,
    verbose=False,
)

# 최적 개체 출력
best_individual = hof.items[0]
print("Best Individual = ", best_individual)
print("Fitness = ", evalTour(best_individual))


def solve_tsp_for_cluster(cluster):
    # 숙소를 포함하여 TSP 문제 설정
    if len(cluster) == 0:
        return [0]  # 군집 내 관광지가 없으면 숙소만 반환
    cluster_with_base = [0] + cluster  # 숙소를 포함
    manager = pywrapcp.RoutingIndexManager(len(cluster_with_base), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    # 거리 콜백
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return (
            moving_time_matrix[cluster_with_base[from_node], cluster_with_base[to_node]]
            + duration_time_list[cluster_with_base[to_node]]
        )

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # TSP 문제 해결
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    )

    solution = routing.SolveWithParameters(search_parameters)
    time = solution.ObjectiveValue()
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(cluster_with_base[manager.IndexToNode(index)])
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route, time  # 숙소에서 시작하고 종료하는 경로 인덱스 반환
    else:
        return [0], time  # 해결할 수 없는 경우 숙소만 반환


# 각 날짜별 군집화된 관광지를 식별하고 TSP 해결
for day in range(total_day):
    # 군집화된 관광지 인덱스 식별
    cluster = [i + 1 for i, cid in enumerate(best_individual) if cid == day]
    if not cluster:
        print(f"Day {day + 1}: No visits planned.")
        continue
    # 해당 군집에 대한 TSP 경로 해결
    tsp_route, total_seconds = solve_tsp_for_cluster(cluster)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    # 경로 출력
    print(f"Day {day+1} Tour Order(with {hours} hours {minutes} minutes):")
    route_names = [travel_point_name[idx] for idx in tsp_route]
    print(" -> ".join(route_names))
    print()
