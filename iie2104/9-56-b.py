import cvxpy as cp

x1 = cp.Variable(integer=True)
x2 = cp.Variable(integer=True)

obj = cp.Maximize(2 * x1 + 3 * x2)
cons = [
    7 * x1 + 5 * x2 <= 36,
    4 * x1 + 9 * x2 <= 35,
    x1 >= 0,
    x2 >= 0,
]
prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value)
print(x2.value)
print(prob.value)
