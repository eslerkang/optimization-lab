import numpy as np
import pandas as pd
from collections import deque

csv_file_path = "./international_airports.csv"
df = pd.read_csv(csv_file_path)

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


def bfs_tsp(distance_matrix, start_index=0):
    n = len(distance_matrix)
    queue = deque([(start_index, [start_index], 0)])
    best_distance = float("inf")
    best_path = None

    while queue:
        current_node, current_path, current_distance = queue.popleft()

        if len(current_path) == n + 1:
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = current_path
            continue

        for next_node in range(n):
            if next_node not in current_path:
                new_path = current_path + [next_node]
                new_distance = (
                    current_distance + distance_matrix[current_node][next_node]
                )

                if len(new_path) == n:
                    new_distance += distance_matrix[next_node][start_index]

                queue.append((next_node, new_path, new_distance))

    return best_path, best_distance


start_index = df[df["Airport"] == "Incheon International Airport"].index[0]
best_solution, best_distance = bfs_tsp(distance_matrix, start_index)

best_route = [df.iloc[i]["Airport"] for i in best_solution]

print("Best route:", best_route)
print("Total distance:", best_distance)
