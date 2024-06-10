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
    cluster_with_base = [0] + cluster + [0]
    if len(cluster_with_base) <= 2:
        return 0

    manager = pywrapcp.RoutingIndexManager(len(cluster_with_base), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

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
        return solution.ObjectiveValue()
    else:
        return 0


# 평가 함수
def evalTour(individual, alpha):
    clusters = [[] for _ in range(total_day)]
    for idx, cluster_id in enumerate(individual):
        clusters[cluster_id].append(idx + 1)

    times = [calculate_cluster_time(cluster) for cluster in clusters]
    total_travel_time = np.sum(times)
    travel_time_std = np.std(times) if len(times) > 1 else 0

    fitness = alpha * total_travel_time + (1 - alpha) * travel_time_std
    return (fitness,)


def run_experiment(alpha):
    toolbox.register("evaluate", evalTour, alpha=alpha)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

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

    best_individual = hof.items[0]
    fitness = evalTour(best_individual, alpha)
    return best_individual, fitness


# 알파 값 범위 설정 및 실험 수행
alpha_values = np.arange(0.0, 1.1, 0.1)
results = []

for alpha in alpha_values:
    best_individual, fitness = run_experiment(alpha)
    results.append((alpha, best_individual, fitness))

# 결과 분석
results_df = pd.DataFrame(results, columns=["Alpha", "Best Individual", "Fitness"])
results_df["Total Travel Time"] = results_df["Best Individual"].apply(
    lambda ind: np.sum(
        [
            calculate_cluster_time([i + 1 for i, cid in enumerate(ind) if cid == day])
            for day in range(total_day)
        ]
    )
)
results_df["Travel Time Std Dev"] = results_df["Best Individual"].apply(
    lambda ind: np.std(
        [
            calculate_cluster_time([i + 1 for i, cid in enumerate(ind) if cid == day])
            for day in range(total_day)
        ]
    )
)

# 결과 표시
print(results_df)
