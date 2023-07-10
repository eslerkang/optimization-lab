import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)
x4 = cp.Variable(nonneg=True)

cons = [
    x1 + 2 * x2 + 2 * x3 + 4 * x4 <= 40,
    2 * x1 - x2 + x3 + 2 * x4 <= 8,
    4 * x1 - 2 * x2 + x3 - x4 <= 10,
]
# obj = cp.Maximize(3 * x1 - x2 + 3 * x3 + 4 * x4)
obj = cp.Minimize(5 * x1 - 4 * x2 + 6 * x3 - 8 * x4)

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, x4.value, prob.value)
