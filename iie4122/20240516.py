import numpy as np
import matplotlib.pyplot as plt


# Random walk function
def random_walk(n_steps):
    # Initialize the starting point
    x, y = 0, 0
    positions = [(x, y)]

    for _ in range(n_steps):
        # Choose a random direction: up, down, left, or right
        direction = np.random.choice(["up", "down", "left", "right"])

        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        positions.append((x, y))

    return positions


# Number of steps
n_steps = 1000

# Generate random walk
walk = random_walk(n_steps)

# Extract the x and y coordinates
x_coords, y_coords = zip(*walk)

# Plot the random walk
plt.figure(figsize=(10, 10))
plt.plot(x_coords, y_coords, marker="o", markersize=2, linestyle="-", color="blue")
plt.title("2D Random Walk")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
