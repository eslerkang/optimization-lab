import numpy as np
import gurobipy as gp
from gurobipy import GRB

max_w_cost = 30000

w_size_capacity = np.array([3000, 5000, 10000])
w_cost = np.array(
    [
        [10000, 15000, 20000],
        [8000, 12000, 17000],
    ]
)
demand = np.array([2000, 2500, 1000, 3500])

c_fw = np.array([10, 15])
c_wr = np.array(
    [
        [2, 3, 5, 4],
        [5, 4, 6, 7],
    ]
)

model = gp.Model("Hw3-2")

y_ws = model.addVars(2, len(w_size_capacity), vtype=GRB.BINARY, name="y_ws")
x_fw = model.addVars(2, vtype=GRB.INTEGER, name="x_fw", lb=0)
x_wr = model.addVars(2, len(demand), vtype=GRB.INTEGER, name="x_wr", lb=0)

for w in range(2):
    model.addConstr(gp.quicksum(y_ws[w, s] for s in range(len(w_size_capacity))) <= 1)

model.addConstr(
    gp.quicksum(
        w_cost[w, s] * y_ws[w, s] for w in range(2) for s in range(len(w_size_capacity))
    )
    <= max_w_cost
)

for w in range(2):
    model.addConstr(
        x_fw[w]
        <= gp.quicksum(
            w_size_capacity[s] * y_ws[w, s] for s in range(len(w_size_capacity))
        )
    )

for w in range(2):
    model.addConstr(x_fw[w] == gp.quicksum(x_wr[w, r] for r in range(len(demand))))

for r in range(len(demand)):
    model.addConstr(gp.quicksum(x_wr[w, r] for w in range(2)) >= demand[r])

model.setObjective(
    gp.quicksum(c_fw[w] * x_fw[w] for w in range(2))
    + gp.quicksum(c_wr[w, r] * x_wr[w, r] for w in range(2) for r in range(len(demand)))
    + gp.quicksum(
        w_cost[w, s] * y_ws[w, s] for w in range(2) for s in range(len(w_size_capacity))
    ),
    GRB.MINIMIZE,
)

model.optimize()

print(f"Objective value: {model.objVal}")


print("\n창고 설치 및 용량:")
for w in range(2):
    for s in range(len(w_size_capacity)):
        if y_ws[w, s].x == 1:
            print(f"창고 {w+1}: 크기 = {w_size_capacity[s]}")


print("\n물류 이송 경로:")


print("\n[공장 -> 창고]")
for w in range(2):
    if x_fw[w].x > 0:
        print(f"공장 -> 창고{w+1}: {x_fw[w].x:.0f}")

print("\n[창고 -> 소매점]")
for w in range(2):
    for r in range(len(demand)):
        if x_wr[w, r].x > 0:
            print(f"창고{w+1} -> 소매점{r+1}: {x_wr[w,r].x:.0f}")
