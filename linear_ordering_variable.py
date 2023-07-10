import cvxpy as cp
import numpy as np

W = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
P = np.array([2, 3, 1, 4, 3])
D = np.array([4, 5, 2, 7, 6])

x = cp.Variable((5, 5), boolean=True)
c = cp.Variable(5)
t = cp.maximum(0, c - D)

obj = cp.Minimize(W.T @ t)
cons = (
    [
        x[i][j] + x[j][k] + x[k][i] <= 2
        for i in range(5)
        for j in range(5)
        for k in range(5)
        if i != j != k
    ]
    + [x[i][j] + x[j][i] == 1 for i in range(5) for j in range(i + 1, 5)]
    + [
        c[i] == cp.sum([P[j] * x[j][i] for j in range(5) if i != j]) + P[i]
        for i in range(5)
    ]
)

prob = cp.Problem(obj, cons)
prob.solve()

print(prob.value)
print(x.value)
print(c.value)
print(t.value)
