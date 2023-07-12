import cvxpy as cp
import numpy as np

W = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
P = np.array([2, 3, 1, 5, 4])
c = cp.Variable(5, nonneg=True)
y = cp.Variable((5, 5), boolean=True)
M = np.sum(P)

obj = cp.Minimize(cp.sum(W.T @ c))
cons = [
    c >= P,
    # c >= P + R,
]

for j in range(5):
    for k in range(j + 1, 5):
        cons.append(c[j] + P[k] <= c[k] + M * (1 - y[j][k]))
        cons.append(c[k] + P[j] <= c[j] + M * y[j][k])

prob = cp.Problem(obj, cons)
prob.solve()

print(prob.value)
print(c.value)
print(y.value)
