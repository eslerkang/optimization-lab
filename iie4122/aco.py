from math import exp, sin

import numpy as np

np.random.seed(486)


class AntColony:
    def __init__(
        self,
        distances,
        n_ants=10,
        n_best=5,
        n_iterations=100,
        alpha=1,
        beta=2,
    ):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for _ in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, _ in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += exp(-self.distances[move]) / (
                    1 + sin(self.distances[move]) ** 2
                )

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        min_dist = np.inf
        move = None
        for i in self.all_inds:
            if i not in visited and dist[i] < min_dist:
                min_dist = dist[i]
                move = i

        return move


if __name__ == "__main__":
    distances = np.array(
        [
            [np.inf, 2, 2, 5, 7],
            [2, np.inf, 4, 8, 2],
            [2, 4, np.inf, 1, 3],
            [5, 8, 1, np.inf, 2],
            [7, 2, 3, 2, np.inf],
        ]
    )
    ant_colony = AntColony(
        distances, n_ants=3, n_best=2, n_iterations=100, alpha=1, beta=2
    )
    shortest_path = ant_colony.run()
    print(f"Shortest Path: {shortest_path}")
