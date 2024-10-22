import cvxpy as cp
from fractions import Fraction

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)

obj = cp.Maximize(9 * x1 + 5 * x2)
cons = [
    4 * x1 + 9 * x2 <= 35,
    x1 <= 6,
    x1 - 3 * x2 >= 1,
    3 * x1 + 2 * x2 <= 19,
    x2 >= 1,
    x1 >= 6,
]

prob = cp.Problem(obj, cons)
prob.solve("GUROBI")

print(x1.value, x2.value, obj.value)
print(
    Fraction(x1.value).limit_denominator(),
    Fraction(x2.value).limit_denominator(),
    Fraction(obj.value).limit_denominator(),
)
