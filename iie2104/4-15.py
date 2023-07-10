import cvxpy as cp

x1 = cp.Variable()
x2 = cp.Variable()

obj = cp.Minimize(3 * x1 + 4 * x2)
cons = [x1 + 2 * x2 >= 1, 2 * x1 - x2 >= 5, x1 >= 3]

prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, obj.value)
