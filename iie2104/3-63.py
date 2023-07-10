import cvxpy as cp

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
obj = cp.Maximize(2 * x1 + 3 * x2)
cons = [
        2 * x1 + 2 * x2 <= 8, 3 * x1 + 6 * x2 <= 18
        ]

prob = cp.Problem(obj, cons)
prob.solve()

print(cons[0].dual_value)
print(cons[1].dual_value)

print(x1.value, x2.value)
