import math, random
import numpy as np


def objective_function(x):
    P_n = x[0]
    m_n = x[1]
    q_i = x[2]
    p_i = x[3]
    s_i = x[4]
    A_i = x[5]
    w_n = [1.5, 1.2, 1]
    wtm_n = [0.25, 0.25, 0.25]
    wem_n = []
    psi_n = [81.54, 81.5, 81.65]
    d_i = [
        3.99 * pow(s_i[i], 0.01) + 2.5 * (770 - p_i[i]) / (p_i[i] - 100)
        for i in range(3)
    ]
    chi_n_i = [[0.33, 0.36, 0.35], [0.32, 0.24, 0.3], [0.35, 0.4, 0.36]]
    D_n = [sum(chi_n_i[n][i] * d_i[i] for i in range(3)) for n in range(3)]
    S_n = [450, 500, 480]
    Q_n = []
    C_n_m = [25, 20, 27]
    C_n_d = [700.45, 1780.13, 1610.89]
    e_n = [1, 1, 1]
    h_m_n = [2.3, 3, 4]
    phi_n = [4, 3, 4.2]
    g_n = [0.9, 0.9, 0.9]
    F_n_c = [1, 1, 1]
    G_n = [1, 1, 1]
    F_n_L = [1, 1, 1]
    wer_i = [1, 1, 1]
    x_n = [7, 6, 7]
    eta_n_M = [0.3, 0.3, 0.3]
    wtr_i = [0.1, 0.1, 0.1]
    v_n = [1, 1, 1]
    f_n = [1, 1, 1]
    C_n_t = [0.5, 0.6, 0.58]
    AA_i = [200, 205, 208]
    eta_i_R = [0.1, 0.1, 0.1]
    c_ri_p = [81.54, 81.5, 81.65]
    d_ri = [1, 1, 1]
    sigma_i = [1, 1, 1]
    h_ri = [1, 1, 1]
    Ce_n_R = [0.1, 0.14, 0.18]
    t_n_S = [1, 1, 1]
    C_i = [1, 1, 1]
    L1_i = [1, 1, 1]
    sigma_i = [1, 1, 1]
    lambda_i_R = [1, 1, 1]
    I_i = [1, 1, 1]
    k_i = [1, 1, 1]
    K_ui = [1, 1, 1]
    X_i = [1, 1, 1]
    R_i = [1, 1, 1]
    K_i = [1, 1, 1]

    return sum(
        (1 - wtm_n[i])
        * (
            wem_n[i] * psi_n[i] * D_n[i]
            - wem_n[i] * S_n[i] * D_n[i] / m_n[i] / Q_n[i]
            - (C_n_m[i] + C_n_d[i] / P_n[i] + e_n[i] * P_n[i])
            * wem_n[i]
            * m_n[i]
            * D_n[i]
            - wem_n[i]
            * h_m_n[i]
            * Q_n[i]
            / 2
            * (m_n[i] * (1 - D_n[i] / P_n[i]) - 1 + 2 * D_n[i] / P_n[i])
            - wem_n[i] * phi_n[i] * D_n[i] * m_n[i] * Q_n[i] * g_n[i] / 2
            - wem_n[i]
            * D_n[i]
            / Q_n[i]
            * (F_n_c[i] * x_n[i] + G_n[i] * (w_n[i] + F_n_L[i]))
            - wem_n[i] * Ce_n_R[i] * x_n[i] * D_n[i] / Q_n[i]
            - wem_n[i] * (1 + eta_n_M[i]) * v_n[i] * D_n[i] / m_n[i] / Q_n[i]
            - (f_n[i] + C_n_t[i] * D_n[i])
        )
        for i in range(3)
    ) + sum(
        (1 - wtr_i[i])
        * wer_i[i]
        * (
            p_i[i] * d_i[i]
            - d_i[i] * (AA_i[i] + eta_i_R[i]) / q_i[i]
            - wer_i[i] * c_ri_p[i] * d_ri[i]
            - h_ri[i]
            * (
                q_i[i] / 2
                + A_i[i]
                * sigma_i[i]
                * math.sqrt(sum(t_n_S[n] + Q_n[n] / m_n[n] / P_n[n] for n in range(3)))
            )
            - d_i[i] * C_i[i] * L1_i[i] / q_i[i]
            - lambda_i_R[i] * d_i[i] / q_i[i]
            - I_i[i] * s_i[i] * s_i[i] / 2
            - (
                k_i[i] * d_i[i] * max(0, (X_i[i] - R_i[i]) / q_i)
                + k_i[i]
                * d_i[i]
                * sum((m_n[n] - 1) * max(0, X_i[i] - R_i[i] ** 2) for n in range(3))
                / q_i[i]
            )
            - Ce_n_R[i] * d_i[i] / q_i[i]
            - d_i[i] * (K_i[i] / q_i[i] + K_ui[i])
        )
        for i in range(3)
    )


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
    bounds = [
        [(-10, 10), (-10, 10), (-10, 10)],
        [(-10, 10), (-10, 10), (-10, 10)],
        [(-10, 10), (-10, 10), (-10, 10)],
        [(-10, 10), (-10, 10), (-10, 10)],
        [(-10, 10), (-10, 10), (-10, 10)],
    ]  # Define bounds for x and y
    num_particles = 50
    maxiter = 100

    best_pos, best_err = PSO(objective_function, bounds, num_particles, maxiter)
    print(f"Best position: {best_pos}")
    print(f"Best error: {best_err}")
