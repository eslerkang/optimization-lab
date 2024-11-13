import numpy as np
import gurobipy as gp
from gurobipy import GRB


demand = np.array([250, 350, 100, 200, 400, 300])

distance_matrix = np.array(
    [
        [0, 6, 2, 5, 4, 4],
        [6, 0, 6, 8, 9, 8],
        [2, 6, 0, 4, 3, 2],
        [5, 8, 4, 0, 7, 6],
        [4, 9, 3, 7, 0, 5],
        [4, 8, 2, 6, 5, 0],
    ]
)

binary_distance_matrix = np.array(
    [
        [1, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1],
    ]
)

nodes = ["A", "B", "C", "D", "E", "F"]

model = gp.Model("hw2-1 - original")

x_i = model.addVars(len(nodes), vtype=GRB.BINARY, name="x_i")
y_i = model.addVars(len(nodes), vtype=GRB.BINARY, name="y_i")

for index, binary_distance in enumerate(binary_distance_matrix):
    model.addConstr(
        gp.quicksum(binary_distance[i] * y_i[i] for i in range(len(nodes)))
        >= x_i[index]
    )

model.addConstr(gp.quicksum(y_i) <= 1)

model.setObjective(
    gp.quicksum(demand[i] * x_i[i] for i in range(len(nodes))), GRB.MAXIMIZE
)

model.optimize()

print(f"Objective value: {model.objVal}")

for v in model.getVars():
    print(f"{v.varName}: {v.x}")


column_elimination_matrix = np.array(
    [
        [1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
    ]
)

model = gp.Model("hw2-1 - column elimination")

x_i = model.addVars(len(nodes), vtype=GRB.BINARY, name="x_i")
y_i = model.addVars(len(nodes), vtype=GRB.BINARY, name="y_i")

for index, binary_distance in enumerate(column_elimination_matrix):
    model.addConstr(
        gp.quicksum(binary_distance[i] * y_i[i] for i in range(len(nodes)))
        >= x_i[index]
    )

model.addConstr(gp.quicksum(y_i) <= 1)

model.setObjective(
    gp.quicksum(demand[i] * x_i[i] for i in range(len(nodes))), GRB.MAXIMIZE
)

model.optimize()

print(f"Objective value: {model.objVal}")

for v in model.getVars():
    print(f"{v.varName}: {v.x}")
