import matplotlib.pyplot as plt

num_workers = [1, 2, 4, 8, 16, 32, 64]

runtimes = [94.1794, 85.8841, 66.3036, 51.0005, 51.3457, 44.2393, 69.1251]

theoretical_speedup = 3.659


t1 = runtimes[0]
speedups = [t1 / t for t in runtimes]

plt.plot(num_workers, speedups, marker='o', color='blue', linestyle='-', label='Measured')

plt.axhline(y=theoretical_speedup, color='red', linestyle='--', label='Amdahl max')

plt.xlabel("Workers")
plt.ylabel("Speedup")
plt.title("Speedup vs. Workers")
plt.xticks(num_workers)
plt.legend(loc='best', frameon=False)
plt.show()

print(f"Total runtime at 64 workers: {runtimes[-1]:.4f} s")
