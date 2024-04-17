import random
import numpy as np

import math


def objective_function(x):
    return np.sin(0.5 * np.pi / (x[0] ** 2 + x[1] ** 2 + 1))


class Particle:
    def __init__(self, bounds):
        self.position_i = np.array(
            [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
        )  # current position
        self.velocity_i = np.array(
            [random.uniform(-1, 1) for _ in range(len(bounds))]
        )  # current velocity
        self.pos_best_i = self.position_i.copy()  # best position individual
        self.err_best_i = float("inf")  # best error individual
        self.err_i = float("inf")  # error individual

    def evaluate(self, objective_function):
        self.err_i = objective_function(self.position_i)
        if self.err_i < self.err_best_i:
            self.pos_best_i = self.position_i.copy()
            self.err_best_i = self.err_i

    def update_velocity(self, pos_best_g):
        w = 0.5  # inertia constant
        c1 = 1.0  # cognative constant
        c2 = 2.0  # social constant

        for i in range(len(self.velocity_i)):
            r1 = random.random()
            r2 = random.random()
            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position_i[i])
            self.velocity_i[i] = w * self.velocity_i[i] + vel_cognitive + vel_social

    def update_position(self, bounds):
        self.position_i += self.velocity_i
        # Apply boundaries
        for i in range(len(bounds)):
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]


# Define the PSO function
def PSO(objective_function, bounds, num_particles, maxiter):
    global num_dimensions

    num_dimensions = len(bounds)
    err_best_g = float("inf")  # best error for group
    pos_best_g = np.zeros(num_dimensions)  # best position for group

    # Initialize swarm
    swarm = [Particle(bounds) for _ in range(num_particles)]

    # Begin optimization
    for i in range(maxiter):
        for particle in swarm:
            particle.evaluate(objective_function)
            # Determine if current particle is the best (globally)
            if particle.err_i < err_best_g:
                pos_best_g = particle.position_i.copy()
                err_best_g = particle.err_i

        # Update velocity and position of particles
        for particle in swarm:
            particle.update_velocity(pos_best_g)
            particle.update_position(bounds)

    return pos_best_g, err_best_g


# Example of running the PSO
if __name__ == "__main__":
    bounds = [(-10, 10), (-10, 10)]  # Define bounds for x and y
    num_particles = 50
    maxiter = 100

    best_pos, best_err = PSO(objective_function, bounds, num_particles, maxiter)
    print(f"Best position: {best_pos}")
    print(f"Best error: {best_err}")
