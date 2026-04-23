import matplotlib.pyplot as plt

num_workers = [1, 2, 4, 8, 16, 32, 64]


# Detta är för f)
runtimes = [75.5345, 51.2901, 40.3619, 36.9829, 32.2387, 32.7451, 30.3308]

theoretical_speedup = 526.3


t1 = runtimes[0]
speedups = [t1 / t for t in runtimes]

plt.plot(num_workers, speedups, marker='o', color='blue', linestyle='-', label='Measured')

# plt.axhline(y=theoretical_speedup, color='red', linestyle='--', label='Amdahl max')

plt.xlabel("Workers")
plt.ylabel("Speedup")
plt.title("Speedup vs. Workers")
plt.xticks(num_workers)
plt.legend(loc='best', frameon=False)
plt.show()

print(f"Total runtime at 64 workers: {runtimes[-1]:.4f} s")
