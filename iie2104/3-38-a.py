import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)

obj = cp.Maximize(2 * x1 + 3 * x2 - 5 * x3)
cons = [x1 + x2 + x3 == 7, 2 * x1 - 5 * x2 + x3 >= 10]

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, prob.value)
