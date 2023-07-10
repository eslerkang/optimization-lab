import cvxpy as cp
import numpy as np

x = cp.Variable(10, integer=True)
y = cp.Variable((10, 10), integer=True)
p = np.array([10, 3, 13, 15, 9, 22, 17, 30, 12, 16])
d = np.array([20, 98, 100, 34, 50, 44, 32, 60, 80, 150])
s = cp.Variable(10)
orcons = (
    [
        100000 * (1 - y[i][j]) >= x[i] + p[i] - x[j]
        for i in range(9)
        for j in range(i + 1, 10)
    ]
    + [
        100000 * y[i][j] >= x[j] + p[j] - x[i]
        for i in range(9)
        for j in range(i + 1, 10)
    ]
    + [y[i][j] == 1 - y[j][i] for i in range(9) for j in range(i + 1, 10)]
)

cons = [
    x >= 0,
    y >= 0,
    y <= 1,
    x - s == d - p,
    y[3][2] <= y[8][6],
] + orcons
obj = cp.Minimize(cp.sum(cp.pos(s)))
prob = cp.Problem(obj, cons)
prob.solve()

print(x.value)
print(y.value)
print(s.value)
print(prob.value)

