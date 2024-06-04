import numpy as np
import matplotlib.pyplot as plt

# 상수값 설정
d = 1  # due slack
q = 2  # q time slack

# K의 범위 설정
K = np.linspace(0, 1, 1000)

# P(K)를 계산
P = np.exp(-K * d) * np.exp(-(1 - K) * q)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(K, P, label="P(K) = exp(-K*d) * exp(-(1-K)*q)")
plt.xlabel("K")
plt.ylabel("Priority (P(K))")
plt.title("Priority as a Function of K")
plt.legend()
plt.grid(True)
plt.axvline(x=0.5, color="r", linestyle="--", label="K = 0.5")
plt.legend()
plt.show()
