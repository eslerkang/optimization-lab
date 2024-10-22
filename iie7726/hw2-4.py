import cvxpy as cp
from fractions import Fraction

x1 = cp.Variable(integer=True)
x2 = cp.Variable(integer=True)
x3 = cp.Variable(integer=True)
x4 = cp.Variable(integer=True)

obj = cp.Maximize(10 * x1 + 12 * x2 + 7 * x3 + 2 * x4)
cons = [
    4 * x1 + 5 * x2 + 3 * x3 + x4 <= 10,
    x1 >= 0,
    x2 >= 0,
    x3 >= 0,
    x4 >= 0,
    x3 <= 1,
    x4 <= 1,
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
