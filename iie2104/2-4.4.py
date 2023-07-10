import cvxpy as cp
import numpy as np

demand = np.array([520, 720, 520, 620])

# Temp worker hiring and firing are set as integer as it deals with # of worker
x_h = cp.Variable(4, integer=True)  # Temp worker hired at the start of the month
x_f = cp.Variable(4, integer=True)  # Temp worker fired at the start of the month
i = cp.Variable(4, nonneg=True)  # Inventory at the end of the month

temps = cp.cumsum(x_h - x_f)  # Temp worker at each month
total_prod = temps * 10 + 12 * 10 + cp.hstack([0, i[:-1]])
# As at the first month, there is no starting inventory. And the Ending inventory is not necessary

obj = cp.Minimize(50 * sum(i) + 200 * sum(x_h) + 400 * sum(x_f))
cons = [
    i == total_prod - demand,
    # As inventory is nonneg, this satisfies total prod >= demand
    temps >= 0,  # Cannot fire more than remaining temp workers
    x_h >= 0,
    x_f >= 0,
]

problem = cp.Problem(obj, cons)
problem.solve(
    verbose=True,
    # solver=cp.GUROBI
)  # verbose setting for checking the procedure

print("x_h: ", x_h.value)
print("x_f: ", x_f.value)
print("i: ", i.value)
print("Z value: ", problem.value)
