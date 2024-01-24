from gurobipy import GRB, Model

# Create a new model
m = Model("hw1")

# Create variables
x_d = m.addVar(name="x1", vtype=GRB.INTEGER)
x_t = m.addVar(name="x2", vtype=GRB.INTEGER)
x_c = m.addVar(name="x3", vtype=GRB.INTEGER)

# Create constraints
m.addConstr(8 * x_d + 6 * x_t + x_c <= 3500, name="lumber")
m.addConstr(4 * x_d + 2 * x_t + 1.5 * x_c <= 1500, name="finishing")
m.addConstr(2 * x_d + 1.5 * x_t + 0.5 * x_c <= 1000, name="carpentry")
m.addConstr(x_d >= 0, name="x_d")
m.addConstr(x_t >= 0, name="x_t")
m.addConstr(x_c >= 0, name="x_c")
m.addConstr(x_d <= (0.3 * 50 + 150 * 0.4 + 0.3 * 250), name="x_d_max")
m.addConstr(x_t <= (0.3 * 20 + 0.4 * 110 + 0.3 * 250), name="x_t_max")
m.addConstr(x_c <= (0.3 * 200 + 0.4 * 225 + 0.3 * 500), name="x_c_max")

m.setObjective(58 * x_d + 36 * x_t + 4.8 * x_c, GRB.MAXIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)
