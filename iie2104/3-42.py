import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)

obj = cp.Maximize(2 * x1 + 5 * x2)
cons = [3 * x1 + 2 * x2 >= 6, 2 * x1 + x2 <= 2]
prob = cp.Problem(obj, cons)
prob.solve()

print(prob.status, x1.value, x2.value, prob.value)
