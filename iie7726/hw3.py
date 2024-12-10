from gurobipy import GRB, Model


model = Model("hw3")
x1 = model.addVar(name="x1", lb=0, vtype=GRB.INTEGER)
x2 = model.addVar(name="x2", lb=0, vtype=GRB.INTEGER)

model.addConstr(x1 + x2 >= 4, name="cons1")
model.addConstr(x1 + 5 * x2 >= 5, name="cons2")
model.setObjective(x1 + 2 * x2, GRB.MINIMIZE)

model.optimize()

print(f"Optimal value: {model.objVal}")
print(f"x1: {x1.x}, x2: {x2.x}")
