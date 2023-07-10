import cvxpy as cp

xb = cp.Variable(nonneg=True)
xa = cp.Variable(nonneg=True)
s1p = cp.Variable(nonneg=True)
s2p = cp.Variable(nonneg=True)
s2m = cp.Variable(nonneg=True)
s3p = cp.Variable(nonneg=True)
s3m = cp.Variable(nonneg=True)

obj = cp.Minimize(s2m)
cons = [
    200 * xb - s1p == 1500,
    100 * xb + 400 * xa - s2p + s2m == 450,
    400 * xa - s3p + s3m == 900,
    1500 * xb + 3000 * xa <= 20000,
]

prob = cp.Problem(obj, cons)
prob.solve()

print("xb: ", xb.value)
print("xa: ", xa.value)
print("s1p: ", s1p.value)
print("s2p: ", s2p.value)
print("s2m: ", s2m.value)
print("s3p: ", s3p.value)
print("s3m: ", s3m.value)
print(prob.value)
