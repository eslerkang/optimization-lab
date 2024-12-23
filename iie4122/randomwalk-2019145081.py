import math, random

import numpy as np
import pandas as pd

random.seed(486)

df = pd.read_csv("./international_airports.csv")

coordinates = df[["Latitude", "Longitude"]].values
n_airports = len(coordinates)


def calculate_distance_matrix(coords):
    n = len(coords)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = np.sqrt(
                (coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2
            )
    return distance_matrix


distance_matrix = calculate_distance_matrix(coordinates)


def calculate_total_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i + 1]]
    total_distance += distance_matrix[path[-1]][path[0]]
    return total_distance


def random_walk_tsp(distance_matrix, start_index=0, n_iter=10000):
    n = len(distance_matrix)

    best_solution = None
    best_distance = math.inf

    for _ in range(n_iter):
        candidate_solution = (
            [start_index] + random.sample(range(1, n), n - 1) + [start_index]
        )
        candidate_distance = calculate_total_distance(
            candidate_solution, distance_matrix
        )

        if candidate_distance < best_distance:
            best_solution = candidate_solution
            best_distance = candidate_distance

    return best_solution, best_distance


start_index = df[df["Airport"] == "Incheon International Airport"].index[0]
best_solution, best_distance = random_walk_tsp(distance_matrix, start_index)

best_route = [df.iloc[i]["Airport"] for i in best_solution]

print("Best route:", best_route)
print("Total distance:", best_distance)
