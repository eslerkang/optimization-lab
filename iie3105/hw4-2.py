from gurobipy import Model, GRB

model = Model("hw4-2")

centers = range(3)
cities = range(4)

capacity = [30, 55, 40]

fixed_cost = [20_000, 30_000, 27_500]

trans_cost = [
    [600, 500, 900, 300],
    [400, 300, 500, 600],
    [500, 800, 200, 400],
]

demand = [11, 18, 15, 25]

y_i = model.addVars(centers, vtype=GRB.BINARY, name="y")

x_ij = model.addVars(centers, cities, vtype=GRB.INTEGER, name="x")

model.setObjective(
    sum(fixed_cost[i] * y_i[i] for i in centers)
    + sum(trans_cost[i][j] * x_ij[i, j] for i in centers for j in cities),
    GRB.MINIMIZE,
)

for j in cities:
    model.addConstr(sum(x_ij[i, j] for i in centers) >= demand[j])

for i in centers:
    model.addConstr(sum(x_ij[i, j] for j in cities) <= capacity[i] * y_i[i])

model.optimize()

print(f"총 비용: ${model.objVal:,.2f}")

print()

for i in centers:
    if y_i[i].x == 1:
        print(f"센터 {i+1}: 개설")
    else:
        print(f"센터 {i+1}: 미개설")

print()

for i in centers:
    for j in cities:
        if x_ij[i, j].x > 0:
            print(f"센터 {i+1} -> 도시 {j+1}: {int(x_ij[i,j].x)} truckloads")
