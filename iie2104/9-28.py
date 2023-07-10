import cvxpy as cp

x1 = cp.Variable(integer=True)
x2 = cp.Variable(integer=True)
x3 = cp.Variable(integer=True)

cons = [
    x1 >= 100,
    x2 >= 150,
    x3 >= 200,
    5.5 * x1 + 3.5 * x2 + 7.5 * x3 <= 3800,
    4.5 * x1 + 3.5 * x2 + 5.5 * x3 <= 2850,
]
obj = cp.Maximize(30 * x1 + 20 * x2 + 40 * x3 - 110 - 90 - 140)
prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value, x2.value, x3.value, prob.value)
