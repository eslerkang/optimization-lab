import cvxpy as cp

xti = cp.Variable((5, 3), nonneg=True)
s = cp.Variable(5, nonneg=True)
obj = cp.Maximize(s[4] + 1.04 * xti[4][0] + 1.09 * xti[3][1])
cons = [
    xti[0][2] == 0,
    xti[2][2] == 0,
    xti[3][2] == 0,
    xti[4][1] == 0,
    xti[4][2] == 0,
    cp.sum(xti[0]) + s[0] == 5000,
] + [
    cp.sum(xti[t]) + s[t]
    == 1.04 * xti[t - 1][0] + 1.09 * xti[t - 2][1] + 1.15 * xti[t - 3][2] + s[t - 1]
    for t in range(1, 5)
]
prob = cp.Problem(objective=obj, constraints=cons)
prob.solve()

print(prob.value)
print(xti.value)
print(s.value)
