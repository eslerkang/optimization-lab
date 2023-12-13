from gurobipy import Model, GRB, quicksum

REQ_resij = [
    [
        [1, 3.5, 3],
        [1.5, 3.5, 3.5],
        [1.5, 4.5, 4],
        [3, 4.5, 4.5],
        [4, 5, 5.5],
    ],
    [
        [4, 7, 7.5],
        [4, 7, 7.5],
        [5, 8, 8.5],
        [6, 9, 9.5],
        [6, 7, 8],
    ],
]
ADVERTISING_REQ_ij = [
    [1, 1.1, 1.3],
    [1.5, 1.1, 1.3],
    [1.1, 1.1, 1.3],
    [1.5, 1.2, 1.3],
    [1.9, 1.9, 1.9],
]

CAPACITY_resj = [
    [12000, 15000, 22000],
    [20000, 40000, 35000],
]
AVERTISING_CAPACITY = 20_000
GRAPHITE_CAPACITY = 16_000

SET_TIME_REQ_j = [65, 60, 65]
SET_TIME_CAPACITY_j = [5_500, 5_000, 6_000]

MIN_DEMAND_ij = [
    [0, 0, 0],
    [100, 100, 50],
    [200, 200, 100],
    [30, 30, 15],
    [100, 100, 100],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

MAX_DEMAND_ij = [
    [2000, 2000, 2000],
    [2000, 2000, 2000],
    [2000, 2000, 2000],
    [2000, 2000, 2000],
    [2000, 2000, 2000],
    [200, 200, 200],
    [100, 100, 100],
    [300, 300, 300],
    [400, 400, 400],
]

COST_ij = [
    [6, 5, 7],
    [19, 18, 20],
    [4, 5, 5],
    [10, 11, 12],
    [26, 24, 27],
    [178, 175, 180],
    [228, 220, 240],
    [350, 360, 370],
    [420, 435, 450],
]

COST_WEIGHT_t = [1, 1.12]

INVENTORY_WEIGHT = 0.08
REVENUE_ij = [
    [10, 10, 12],
    [25, 25, 30],
    [8, 8, 10],
    [18, 18, 22],
    [40, 40, 45],
    [290, 290, 310],
    [380, 380, 420],
    [560, 560, 640],
    [650, 650, 720],
]

m = Model()

x_ijt = m.addVars(9, 3, 2)
inventory_ijt = m.addVars(9, 3, 2)
sold_ijt = m.addVars(9, 3, 2)

m.addConstrs(
    quicksum([x_ijt[i, j, t] * REQ_resij[res][i][j] for i in range(5)])
    + 13
    * (
        REQ_resij[res][0][j] * (x_ijt[5, j, t] + x_ijt[6, j, t])
        + REQ_resij[res][1][j] * (x_ijt[7, j, t] + x_ijt[8, j, t])
    )
    + 3
    * (
        REQ_resij[res][3][j] * (x_ijt[5, j, t] + x_ijt[7, j, t])
        + REQ_resij[res][4][j] * (x_ijt[6, j, t] + x_ijt[8, j, t])
    )
    + 10 * quicksum([x_ijt[i, j, t] * REQ_resij[res][2][j] for i in range(5, 9)])
    <= CAPACITY_resj[res][j]
    for res in range(2)
    for j in range(3)
    for t in range(2)
)
m.addConstrs(
    quicksum(
        quicksum([x_ijt[i, j, t] * ADVERTISING_REQ_ij[i][j] for i in range(5)])
        + 13
        * (
            ADVERTISING_REQ_ij[0][j] * (x_ijt[5, j, t] + x_ijt[6, j, t])
            + ADVERTISING_REQ_ij[1][j] * (x_ijt[7, j, t] + x_ijt[8, j, t])
        )
        + 3
        * (
            ADVERTISING_REQ_ij[3][j] * (x_ijt[5, j, t] + x_ijt[7, j, t])
            + ADVERTISING_REQ_ij[4][j] * (x_ijt[6, j, t] + x_ijt[8, j, t])
        )
        + 10
        * quicksum([x_ijt[i, j, t] * ADVERTISING_REQ_ij[2][j] for i in range(5, 9)])
        for j in range(3)
    )
    <= AVERTISING_CAPACITY
    for t in range(2)
)
m.addConstrs(
    4
    * quicksum(
        x_ijt[1, j, t] + 13 * quicksum([x_ijt[i, j, t] for i in range(7, 9)])
        for j in range(3)
    )
    <= GRAPHITE_CAPACITY
    for t in range(2)
)
m.addConstrs(
    sold_ijt[i, j, t] >= MIN_DEMAND_ij[i][j]
    for i in range(9)
    for j in range(3)
    for t in range(2)
)
m.addConstrs(
    sold_ijt[i, j, t] <= MAX_DEMAND_ij[i][j]
    for i in range(9)
    for j in range(3)
    for t in range(2)
)
m.addConstrs(
    inventory_ijt[i, j, 0] == x_ijt[i, j, 0] - sold_ijt[i, j, 0]
    for i in range(9)
    for j in range(3)
)
m.addConstrs(
    inventory_ijt[i, j, 1]
    == inventory_ijt[i, j, 0] + x_ijt[i, j, 1] - sold_ijt[i, j, 1]
    for i in range(9)
    for j in range(3)
)
m.setObjective(
    quicksum(
        [
            sold_ijt[i, j, t] * REVENUE_ij[i][j]
            for i in range(9)
            for j in range(3)
            for t in range(2)
        ]
    )
    - quicksum(
        [
            x_ijt[i, j, t] * COST_ij[i][j] * COST_WEIGHT_t[t]
            for i in range(9)
            for j in range(3)
            for t in range(2)
        ]
    )
    - quicksum(
        [
            inventory_ijt[i, j, t] * COST_ij[i][j] * COST_WEIGHT_t[t] * INVENTORY_WEIGHT
            for i in range(9)
            for j in range(3)
            for t in range(2)
        ]
    ),
    GRB.MAXIMIZE,
)

m.optimize()

for t in range(2):
    for i in range(9):
        row_values = [
            [x_ijt[i, j, t].X, sold_ijt[i, j, t].X, inventory_ijt[i, j, t].X]
            for j in range(3)
        ]
        print(
            " ".join(
                f"{value[0]:8.2f}({value[1]:8.2f}, {value[2]:8.2f})"
                for value in row_values
            )
        )
    print()
