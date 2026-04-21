import matplotlib.pyplot as plt

num_workers = [1, 2, 4, 8, 16, 32, 64]

runtimes = [637.0487, 428.3166, 422.3446, 333.7244, 323.8274, 310.5394, 297.1898]

theoretical_speedup = 24.5867


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
