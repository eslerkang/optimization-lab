import numpy as np
from gurobipy import GRB, Model

resource = np.array([[8, 6, 1], [4, 2, 1.5], [2, 1.5, 0.5]])
available = np.array([3500, 1500, 1000])
profit = np.array([58, 36, 4.8])
demand = np.array([150, 125, 300])

# Create a new model
m = Model("hw1")

# Create variables
x = m.addMVar((3,), name="x")

# Create constraints
m.addConstr(resource @ x <= available, name="resource")
m.addConstr(x <= demand, name="demand")
m.addConstr(x >= 0, name="x")

m.setObjective(profit @ x, GRB.MAXIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)

print()

# Sensitivity analysis
print("Sensitivity Analysis:")
for c in m.getConstrs():
    print(c.ConstrName, c.Pi)
