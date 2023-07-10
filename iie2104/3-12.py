import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)
x4 = cp.Variable(nonneg=True)
# s1 = cp.Variable(nonneg=True)
# s2 = cp.Variable(nonneg=True)

# constraints = [
#     x1 + 4 * x2 - 2 * x3 + 8 * x4 + s1 == 2,
#     -x1 + 2 * x2 + 3 * x3 + 4 * x4 + s2 == 1,
# ]

# obj = cp.Maximize(2 * x1 - 4 * x2 + 5 * x3 - 6 * x4)

constraints = [x1 + 2 * x2 - 3 * x3 + x4 == 4, x1 + 2 * x2 + x3 + 2 * x4 == 4]
obj = cp.Minimize(x1 + 2 * x2 - 3 * x3 - 2 * x4)

prob = cp.Problem(obj, constraints)
prob.solve()

# print(x1.value, x2.value, x3.value, x4.value, s1.value, s2.value, prob.value)
print(x1.value, x2.value, x3.value, x4.value, prob.value)
