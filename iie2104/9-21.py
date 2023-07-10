import cvxpy as cp

x1 = cp.Variable(integer=True)
x2 = cp.Variable(integer=True)
x3 = cp.Variable(integer=True)
x4 = cp.Variable(integer=True)
x5 = cp.Variable(integer=True)
x6 = cp.Variable(integer=True)

cons = [
    x1 >= 0,
    x2 >= 0,
    x3 >= 0,
    x4 >= 0,
    x5 >= 0,
    x6 >= 0,
    x1 <= 1,
    x2 <= 1,
    x3 <= 1,
    x4 <= 1,
    x5 <= 1,
    x6 <= 1,
    x1 + x4 >= 1,
    x2 + x4 + x6 >= 1,
    x3 + x5 >= 1,
    x1 + x2 + x4 + x6 >= 1,
    x3 + x5 + x6 >= 1,
    x2 + x4 + x5 + x6 >= 1,
]
obj = cp.Minimize(x1 + x2 + x3 + x4 + x5 + x6)
prob = cp.Problem(obj, cons)
prob.solve()

print(x1.value)
print(x2.value)
print(x3.value)
print(x4.value)
print(x5.value)
print(x6.value)
