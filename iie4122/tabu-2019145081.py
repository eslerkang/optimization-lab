import numpy as np
import pandas as pd
from itertools import permutations
from collections import deque
import random

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


def tabu_search(distance_matrix, n_iter=1000, tabu_size=100):
    n = len(distance_matrix)

    current_solution = list(range(n))
    current_distance = calculate_total_distance(current_solution, distance_matrix)

    best_solution = current_solution.copy()
    best_distance = current_distance

    tabu_list = deque(maxlen=tabu_size)

    for _ in range(n_iter):
        neighborhood = []
        for i in range(n):
            for j in range(i + 1, n):
                neighbor = current_solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                if neighbor not in tabu_list:
                    neighborhood.append(
                        (neighbor, calculate_total_distance(neighbor, distance_matrix))
                    )

        neighborhood.sort(key=lambda x: x[1])
        best_candidate, best_candidate_distance = neighborhood[0]

        current_solution = best_candidate
        current_distance = best_candidate_distance

        tabu_list.append(current_solution)

        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance

    return best_solution, best_distance


def calculate_total_distance(solution, distance_matrix):
    total_distance = 0
    for i in range(len(solution) - 1):
        total_distance += distance_matrix[solution[i]][solution[i + 1]]
    total_distance += distance_matrix[solution[-1]][solution[0]]
    return total_distance


best_solution, best_distance = tabu_search(distance_matrix)


best_route = [df.iloc[i]["Airport"] for i in best_solution]


print("Best route:", best_route)
print("Total distance:", best_distance)
