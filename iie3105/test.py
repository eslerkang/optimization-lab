import numpy as np
import matplotlib.pyplot as plt
from fitter import Fitter

# fmt: off
demand = [
    11, 7, 4, 8, 5, 8, 14, 6, 31, 7, 7, 19, 5, 6, 7, 5, 14, 25, 2, 4, 11, 22, 8, 10, 11, 16, 17, 12, 7, 4, 25, 2, 14, 13, 25, 13, 8, 17, 24, 6, 19, 33, 7, 18, 12, 7, 3, 25, 15, 38, 28, 22, 5, 22, 6, 10, 14, 23, 40, 18, 15, 41, 30, 23, 17, 28, 33, 28, 17, 55, 15, 35, 50, 39, 50, 35, 45, 69, 38, 23, 19, 42, 39, 27, 19, 22, 32, 27, 36, 50, 27, 56, 43, 37, 39, 56, 38, 32, 34, 40, 30, 42, 31, 56, 26, 42, 59, 37, 50, 51, 63, 53, 24, 61, 44, 58, 103, 22, 52, 64, 55, 60, 53, 58, 30, 72, 53, 78, 64, 62, 75, 40, 129, 64, 79, 69, 49, 45, 43, 62, 52, 48, 83, 45, 42, 83, 57,
    61, 81, 59, 51, 68, 101, 80, 43, 64, 89, 94, 49, 77, 74, 56, 54, 67, 83, 56, 70, 58, 76, 74, 46, 80, 48, 67, 104, 41, 81, 70, 69, 133, 56, 56, 88, 64, 58, 80, 96, 60, 100, 74, 44, 77, 99, 109, 62, 70, 56, 74, 60, 36, 72, 78, 62, 84, 81, 67, 92, 110, 41, 57, 52, 96, 65, 88, 44, 65, 76, 73, 64, 40, 64, 56, 78, 43, 78, 64, 67, 80, 40, 71, 84, 29, 53, 72, 39, 63, 83, 31, 57, 44, 34, 97, 30, 42, 83, 29, 73, 67, 42, 67, 32, 37, 44, 58, 50, 34, 69, 47, 44, 46, 45, 77, 74, 42, 22, 88, 70, 43, 47, 46, 44, 53, 38, 44, 37, 10, 40, 26, 16, 24, 38, 33, 38, 67, 22, 12, 33,
    33, 44, 27, 58, 20, 29, 18, 62, 10, 4, 23, 14, 34, 10, 10, 14, 16, 10, 18, 12, 36, 20, 3, 12, 18, 9, 6, 26, 13, 16, 10, 7, 6, 20, 13, 6, 38, 18, 7, 6, 5, 13, 19, 24, 6, 18, 2, 10, 12, 11, 5, 4, 26, 2, 14, 31, 28, 5, 3, 4, 4, 10, 3, 2, 3, 29, 15, 4, 5, 7, 1, 41, 3, 3, 6, 12, 10, 14, 5, 4, 9, 9, 1, 29, 6, 4, 1, 13, 2, 2, 26, 6, 2, 18, 11, 9, 7, 31, 18, 30, 2, 8, 15, 26, 6, 16, 13, 10, 4, 21, 11, 5, 4, 18, 21, 24, 4, 5, 12, 18, 10, 9, 33, 22, 63, 25, 19, 20, 15, 21, 25, 15, 23, 16, 19, 18, 22, 23, 27, 19, 47, 15, 5, 17, 39, 16, 43, 19, 51, 27, 28, 48, 14, 26, 46, 38, 13, 19, 48, 37, 49, 40, 49, 37, 38, 46, 31, 41, 16, 23, 26, 40, 47, 25, 26, 51, 28, 46, 45, 43, 26, 50, 26, 64, 33, 57, 38, 36, 40, 36, 79, 43, 47, 57, 37, 30, 38, 79, 46, 42, 43, 58, 49, 42, 59, 72, 48, 55, 59, 32, 32, 92, 51, 39, 24, 71, 88, 38, 59, 55, 55, 75, 28, 90, 27, 32, 58, 78, 48, 97, 106, 53, 43, 59, 28, 70, 72, 80, 53, 52, 64, 66, 62, 66, 94, 88, 37, 71, 89, 83, 72, 86, 53, 72, 107, 42, 76, 44, 45, 63, 53, 98, 89, 92, 51, 79, 95, 108, 61, 47, 73, 64, 45, 64, 74, 75, 59, 52, 71, 44, 59, 48, 76, 62, 41, 49, 72, 81, 101, 103, 35, 96, 77, 57, 81, 74, 52, 73, 58, 93, 33, 42, 59, 75, 34, 77, 64, 57, 91, 74, 84, 30, 35, 45, 55, 53, 64, 56, 75, 80, 30, 60, 71, 60, 50, 66, 67, 46, 48, 71, 68, 22, 36, 41, 36, 58, 63, 29, 29, 42, 75, 85, 61, 47, 39, 49, 54, 25, 32, 31, 36, 48, 32, 50, 21, 34, 49, 18, 33, 30, 35, 18, 33, 26, 34, 34, 30, 37, 65, 16, 15, 17, 14, 54, 17, 33, 12, 15, 21, 16, 24, 19, 10, 26, 39, 23, 14, 16, 26, 21, 29, 7, 13, 40, 4, 22, 9, 11, 29, 13, 56, 12, 19, 12, 26, 11, 21, 9, 11, 6, 8, 10, 12, 3, 38, 11, 13, 2, 23, 9, 5, 10, 9, 10, 11, 9, 5, 6, 27, 3, 1, 4, 27, 2, 13, 1, 27, 3, 17, 2, 8, 4, 10
]
# fmt: on

# Calculate basic statistics
mean_demand = np.mean(demand)
median_demand = np.median(demand)
std_demand = np.std(demand)

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(demand, bins=20, edgecolor="black", density=True, alpha=0.7)
plt.title("Histogram of Demand with Fitted Distributions")
plt.xlabel("Demand")
plt.ylabel("Density")

# Add vertical lines for mean and median
plt.axvline(
    mean_demand,
    color="red",
    linestyle="dashed",
    linewidth=2,
    label=f"Mean: {mean_demand:.2f}",
)
plt.axvline(
    median_demand,
    color="green",
    linestyle="dashed",
    linewidth=2,
    label=f"Median: {median_demand:.2f}",
)

# fmt: off
# Fit distributions using Fitter
f = Fitter(
    demand,
    distributions=[
        "alpha", "chi", "chi2", "erlang", "expon", "exponnorm", "exponweib", "exponpow", "f", "fatiguelife", "fisk", "gamma", "gengamma", "genexpon", "genextreme", "gilbrat", "gompertz", "gumbel_r", "halfcauchy", "halflogistic", "halfnorm", "invgamma", "invgauss", "invweibull", "levy", "loggamma", "lognorm", "lomax", "maxwell", "nakagami", "ncx2", "ncf", "nct", "pareto", "rayleigh", "rice", "truncexpon", "wald", "weibull_min"
    ],
)
# fmt: on
f.fit()

print(f.summary())

# Get the best fitting distribution
best_fit = f.get_best()

# Plot the best fitting distribution
# Get the top 5 best fitting distributions
top_5_fits = sorted(best_fit.items(), key=lambda x: x[1])[:5]

print("Top 5 best fitting distributions:")
for i, (dist_name, params) in enumerate(top_5_fits, 1):
    print(f"{i}. {dist_name}")
    for param_name, param_value in params.items():
        print(f"   {param_name}: {param_value}")
    print()

plt.legend()
plt.show()