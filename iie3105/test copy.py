import numpy as np
import matplotlib.pyplot as plt
from fitter import Fitter

# fmt: off
demand = [
   # Demand data
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
