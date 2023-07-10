import cvxpy as cp
import numpy as np

W = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
P = np.array([2, 3, 1, 4, 3])
D = np.array([4, 5, 2, 7, 6])
T = np.sum(P)
T_INDEX = np.arange(0, T)

x = cp.Variable((5, T), boolean=True)
c = cp.Variable(5)
tar = cp.maximum(0, c - D)

obj = cp.Minimize(W.T @ tar)
cons = [
    cp.sum(x, axis=1) == 1,
]

for j in range(5):
    cons.append(c[j] == cp.sum((T_INDEX + P[j]) @ x[j]))

for i in T_INDEX:
    total = []
    for j in range(5):
        total.append(cp.sum(x[j, max(0, i - P[j] + 1) : i + 1]))
    cons.append(cp.sum(total) <= 1)

prob = cp.Problem(obj, cons)
prob.solve()

print(prob.value)
print(x.value)
print(c.value)
print(tar.value)
