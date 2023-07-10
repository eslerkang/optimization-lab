import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)
x4 = cp.Variable(nonneg=True)

y1 = cp.Variable(nonneg=True)
y2 = cp.Variable(nonneg=True)

obj = cp.Minimize(4 * x1 + 5 * x2 + 8 * x3 + 12 * x4)
# obj = cp.Maximize(y1 + 3 * y2)
cons = [
    -x1 + x2 + x3 + 2 * x4 >= 1,
    2 * x1 + x2 + x3 - 3 * x4 >= 3,
    # -y1 + 2 * y2 <= 4,
    # y1 + y2 <= 5,
    # 2 * y1 - 3 * y2 <= 12,
]

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, x4.value)
# print(y1.value, y2.value)
