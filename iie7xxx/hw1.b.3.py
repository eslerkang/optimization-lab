from gurobipy import GRB, Model

desks = [50, 150, 250]
tables = [20, 110, 250]
chairs = [200, 225, 500]

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
m.addConstrs((x_d <= desk for desk in desks), name="x_d_max")
m.addConstrs((x_t <= table for table in tables), name="x_t_max")
m.addConstrs((x_c <= chair for chair in chairs), name="x_c_max")

m.setObjective(17.6 * x_d + 12.2 * x_t - 0.6 * x_c, GRB.MAXIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)
