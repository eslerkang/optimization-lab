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

unit_cost = np.array([2, 4, 5.2])
resource_use = np.array([[8, 6, 1], [4, 2, 1.5], [2, 1.5, 0.5]])
prod_cost = unit_cost @ resource_use
available = np.array([3500, 1500, 1000])
selling_price = np.array([60, 40, 10])

# Create a new model
m = Model("hw1")

# Create variables
x = m.addMVar((3, 27), name="x", vtype=GRB.INTEGER)
r = m.addMVar((3,), name="r", vtype=GRB.INTEGER)

# Create constraints
m.addConstr(r <= available, name="resource")
m.addConstrs((x[:, s] @ resource_use <= r for s in range(27)), name="resource")
m.addConstrs((x[:, s] <= demand_s[s] for s in range(27)), name="demand")

m.setObjective(
    quicksum(selling_price @ x[:, s] * p_s[s] for s in range(27)) - unit_cost @ r,
    GRB.MAXIMIZE,
)

m.optimize()


for s in range(27):
    print("s =", s)
    print("p =", p_s[s])
    print("x =", x.x[:, s])
    print("r =", r.x)
    print("demand =", demand_s[s])
    print()
