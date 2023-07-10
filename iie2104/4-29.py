import cvxpy as cp

x1 = cp.Variable()
x2 = cp.Variable()
x3 = cp.Variable()
x4 = cp.Variable()

obj = cp.Maximize(9.4 * x1 + 10.8 * x2 + 8.75 * x3 + 7.8 * x4)
# obj = cp.Minimize(4800 * x1 + 9600 * x2 + 4700 * x3 + 4500 * x4)
cons = [
    10.5 * x1 + 9.3 * x2 + 11.6 * x3 + 8.2 * x4 <= 4800,
    20.4 * x1 + 24.6 * x2 + 17.7 * x3 + 26.5 * x4 <= 9600,
    3.2 * x1 + 2.5 * x2 + 3.6 * x3 + 5.5 * x4 <= 4700,
    5 * x1 + 5 * x2 + 5 * x3 + 5 * x4 <= 4500,
    x1 >= 0,
    x2 >= 0,
    x3 >= 0,
    x4 >= 0,
]
# cons = [
#     10.5 * x1 + 20.4 * x2 + 3.2 * x3 + 5 * x4 >= 9.4,
#     9.3 * x1 + 24.6 * x2 + 2.5 * x3 + 5 * x4 >= 10.8,
#     11.6 * x1 + 17.7 * x2 + 3.6 * x3 + 5 * x4 >= 8.75,
#     8.2 * x1 + 26.5 * x2 + 5.5 * x3 + 5 * x4 >= 7.8,
#     x1 >= 0,
#     x2 >= 0,
#     x3 >= 0,
#     x4 >= 0,
# ]

prob = cp.Problem(obj, cons)
prob.solve()

print(f"x1: {x1.value:.2f}")
print(f"x2: {x2.value:.2f}")
print(f"x3: {x3.value:.2f}")
print(f"x4: {x4.value:.2f}")
print(f"obj: {obj.value:.2f}")

print(f"splicing dual price: {cons[0].dual_value:.2f}")
print(f"soldering dual price: {cons[1].dual_value:.2f}")
print(f"sleeving dual price: {cons[2].dual_value:.2f}")
print(f"inspection dual price: {cons[3].dual_value:.2f}")

print(f"x1 dual price: {cons[4].dual_value:.2f}")
print(f"x2 dual price: {cons[5].dual_value:.2f}")
print(f"x3 dual price: {cons[6].dual_value:.2f}")
print(f"x4 dual price: {cons[7].dual_value:.2f}")

for i, con in enumerate(cons):
    print(con.dual_value)
