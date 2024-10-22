import cvxpy as cp
from fractions import Fraction

x1 = cp.Variable(nonneg=True)
x2 = cp.Variable(nonneg=True)
x3 = cp.Variable(nonneg=True)
x4 = cp.Variable(nonneg=True)

obj = cp.Maximize(17 * x1 + 10 * x2 + 25 * x3 + 17 * x4)
cons = [
    5 * x1 + 3 * x2 + 8 * x3 + 7 * x4 <= 12,
    x1 <= 1,
    x2 <= 1,
    x3 == 0,
    x4 == 1,
]

prob = cp.Problem(obj, cons)
prob.solve("GUROBI")

print(x1.value, x2.value, x3.value, x4.value, obj.value)
print(
    Fraction(x1.value).limit_denominator(),
    Fraction(x2.value).limit_denominator(),
    Fraction(x3.value).limit_denominator(),
    Fraction(x4.value).limit_denominator(),
    Fraction(obj.value).limit_denominator(),
)
