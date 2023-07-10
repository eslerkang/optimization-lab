import cvxpy as cp

x1 = cp.Variable()
x2 = cp.Variable(nonneg=True)

obj = cp.Maximize(x1 + 3 * x2)
cons = [x1 + x2 <= 2, -x1 + x2 <= 4]
prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, prob.value)
