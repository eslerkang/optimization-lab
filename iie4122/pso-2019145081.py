import math, random
import numpy as np


def objective_function(x):
    n = x[0]
    I_B = x[1]
    Y = x[2]
    lambda_11 = x[3]
    lambda_12 = x[4]
    S_1on = x[5]
    S_1off = x[6]
    S_2on = x[7]
    S_2off = x[8]

    alpha_1on = 0.2
    alpha_1off = 0.2
    alpha_2on = 0.35
    alpha_2off = 0.25
    c_11 = 0.01
    c_12 = 0.03
    lambda_11_g = 1
    lambda_12_g = 1
    ksi_1 = 150
    ksi_2 = 155
    c_21 = 100
    c_22 = 105
    Gamma_O2O = 1
    A_m = 120
    A_m_prime = 2
    X_m = 150
    mu = 0.4
    X_m_prime = 10
    H_c1 = 5
    H_c2 = 7
    H_D1 = 0.2
    H_D2 = 0.3
    H_c_prime = 0.08
    V_1 = 0.02
    V_2 = 0.02
    Z_1 = 0.02
    Z_2 = 0.02
    E_beta_i = 0.01
    R_1 = 30
    R_2 = 30
    R_1_prime = 0.1
    R_2_prime = 0.1
    h_1 = 10
    h_2 = 15
    C_h_1_prime = 0.5
    lambda_21 = 111
    lambda_22 = 108
    C_h_2_prime = 0.6
    C_h_21_prime = 0.8
    C_h_22_prime = 0.7
    h_21 = 70
    h_22 = 68
    C_h_11_prime = 0.7
    C_h_12_prime = 0.5
    C_E = 2.48
    C_E_prime = 0.2
    sum_f = 155
    sum_E_hp = 2.18
    seta_1 = 10
    sum_area = 145_450
    sum_M = 150
    sum_J = 150
    sum_E_bulb = 20
    seta_2 = 10
    rho = 100
    U_tr = 1200
    v = 15
    F_wifi = 700
    U_l = 1000
    s = 4
    U_sw = 1
    G_B = 3 * 10**5
    P_B = 0.02
    C_D_prime = 0.07
    h_11 = 30
    h_12 = 31
    delta = 0.83

    fit = (
        (
            alpha_1on * S_1on
            + alpha_1off * S_1off
            + alpha_2on * S_2on
            + alpha_2off * S_2off
            - (c_11 * np.power(lambda_11, delta) + ksi_1 / lambda_11 + c_21) * Gamma_O2O
            - (c_12 * np.power(lambda_12, delta) + ksi_2 / lambda_12 + c_22) * Gamma_O2O
        )
        - (
            (A_m + A_m_prime) / Y
            + (X_m * math.exp(-mu * I_B) + X_m_prime) / Y
            + I_B
            + (n * H_c1 / Y + H_D1 * Gamma_O2O) * H_c_prime
            + (V_1 + Z_1 * E_beta_i) * Gamma_O2O
            + (R_1 + R_1_prime) * (E_beta_i * Gamma_O2O)
            + (h_1 + C_h_1_prime)
            / 2
            * (
                Gamma_O2O * Y * (1 - 1 / n)
                + Gamma_O2O * Gamma_O2O * Y / n / lambda_11
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i / lambda_21 * (1 + 1 / n)
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i * E_beta_i / lambda_21
            )
            + (h_21 + C_h_21_prime)
            / 2
            * (
                Gamma_O2O * Y / n
                + Gamma_O2O * Gamma_O2O * Y / lambda_11 * (1 - 1 / n)
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i / lambda_21 * (1 - 1 / n)
            )
            + (h_11 + C_h_11_prime)
            * Gamma_O2O
            * Gamma_O2O
            * Y
            * E_beta_i
            / 2
            / lambda_21
            + (C_E + C_E_prime)
            * sum_f
            * sum_E_hp
            * 746
            * seta_1
            * 365
            / 1000
            / Y
            / sum_area
            + (C_E + C_E_prime)
            * sum_M
            * sum_J
            * sum_E_bulb
            * seta_2
            * 365
            / 1000
            / Y
            / sum_area
        )
        - (
            (A_m + A_m_prime) / Y
            + (X_m * math.exp(-mu * I_B) + X_m_prime) / Y
            + I_B
            + (n * H_c2 / Y + H_D2 * Gamma_O2O) * H_c_prime
            + (V_2 + Z_2 * E_beta_i) * Gamma_O2O
            + (R_2 + R_2_prime) * (E_beta_i * Gamma_O2O)
            + (h_2 + C_h_2_prime)
            / 2
            * (
                Gamma_O2O * Y * (1 - 1 / n)
                + Gamma_O2O * Gamma_O2O * Y / n / lambda_12
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i / lambda_22 * (1 + 1 / n)
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i * E_beta_i / lambda_22
            )
            + (h_22 + C_h_22_prime)
            / 2
            * (
                Gamma_O2O * Y / n
                + Gamma_O2O * Gamma_O2O * Y / lambda_12 * (1 - 1 / n)
                + Gamma_O2O * Gamma_O2O * Y * E_beta_i / lambda_22 * (1 - 1 / n)
            )
            + (h_12 + C_h_12_prime)
            * Gamma_O2O
            * Gamma_O2O
            * Y
            * E_beta_i
            / 2
            / lambda_22
            + (C_E + C_E_prime)
            * sum_f
            * sum_E_hp
            * 746
            * seta_1
            * 365
            / 1000
            / Y
            / sum_area
            + (C_E + C_E_prime)
            * sum_M
            * sum_J
            * sum_E_bulb
            * seta_2
            * 365
            / 1000
            / Y
            / sum_area
        )
    ) - (
        rho * U_tr + (rho - v) * F_wifi + v * U_l + v / s * U_sw + G_B * P_B + C_D_prime
    ) / Y

    return fit


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
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
        (0, 10),
    ]
    num_particles = 50
    maxiter = 100

    best_pos, best_err = PSO(objective_function, bounds, num_particles, maxiter)
    print(f"Best position: {best_pos}")
    print(f"Best error: {best_err}")
