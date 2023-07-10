import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)

obj = cp.Maximize(x1 + 2 * x2 + 3 * x3)
cons = [x1 + 2 * x2 + 3 * x3 <= 10, x1 + x2 <= 5, x1 <= 1]

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, prob.value)
