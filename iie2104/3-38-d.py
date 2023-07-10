import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)
e = cp.Variable(nonneg=True)

obj = cp.Minimize(4 * x1 - 8 * x2 + 3 * x3)
cons = [x1 + x2 + x3 == 7, 2 * x1 - 5 * x2 + x3 - e == 10]

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, e.value, prob.value)
