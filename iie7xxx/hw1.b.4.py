import numpy as np
from gurobipy import GRB, Model, quicksum

desks = [50, 150, 250]
tables = [20, 110, 250]
chairs = [200, 225, 500]
p = [0.3, 0.4, 0.3]

demand_s = np.array(
    [[desk, table, chair] for desk in desks for table in tables for chair in chairs]
)
p_s = np.array([p_d * p_t * p_c for p_d in p for p_t in p for p_c in p])

resource = np.array([[8, 6, 1], [4, 2, 1.5], [2, 1.5, 0.5]])
available = np.array([3500, 1500, 1000])
profit = np.array([58, 36, 4.8])
cost = np.array([2, 4, 5.2])

# Create a new model
m = Model("hw1")

# Create variables
x = m.addMVar((3,), name="x", vtype=GRB.INTEGER)
y = m.addMVar((3, 27), vtype=GRB.INTEGER, name="y")

# Create constraints
m.addConstr(resource @ x <= available, name="resource")
m.addConstrs((x - y[:, s] <= demand_s[s] for s in range(27)), name="demand")
m.addConstr(x >= 0, name="x")

m.setObjective(
    profit @ x - quicksum(cost @ y[:, s] * p_s[s] for s in range(27)), GRB.MAXIMIZE
)

m.optimize()


for s in range(27):
    print("s =", s)
    print("p =", p_s[s])
    print("x =", x.x)
    print("demand =", demand_s[s])
    print("y =", y[:, s].x)
    print()
