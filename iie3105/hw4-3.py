from gurobipy import Model, GRB
import math

model = Model("hw4-3")

east_west = [80, 10, 60, 30, 85, 15]
north_south = [95, 15, 70, 10, 75, 30]
points = range(6)

dist = {}
for i in points:
    for j in points:
        if i != j:
            dist[i, j] = round(
                math.sqrt(
                    (east_west[i] - east_west[j]) ** 2
                    + (north_south[i] - north_south[j]) ** 2
                )
            )

x = model.addVars(
    [(i, j) for i in points for j in points if i != j], vtype=GRB.BINARY, name="x"
)

model.setObjective(
    sum(dist[i, j] * x[i, j] for i in points for j in points if i != j), GRB.MINIMIZE
)

for i in points:
    model.addConstr(sum(x[i, j] for j in points if i != j) == 1)

for j in points:
    model.addConstr(sum(x[i, j] for i in points if i != j) == 1)

u = model.addVars(points, lb=0, name="u")
n = len(points)
for i in points:
    if i != 0:
        model.addConstr(u[i] <= n - 1)
    for j in points:
        if i != j and (i != 0 and j != 0):
            model.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)

model.optimize()

print("\n=== 최적 경로 ===")
print(f"총 이동 거리: {model.objVal:.0f} 단위")

current = 0
route = [0]
while len(route) < len(points):
    for j in points:
        if j not in route and x[current, j].x > 0.5:
            route.append(j)
            current = j
            break

route.append(0)

print("\n상세 경로:")
for i in range(len(route) - 1):
    print(f"지점 {route[i]} -> 지점 {route[i+1]}: {dist[route[i],route[i+1]]} 단위")
