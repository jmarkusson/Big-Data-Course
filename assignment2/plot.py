import matplotlib.pyplot as plt

num_workers = [1, 2, 4, 8, 16, 32, 64]

runtimes = [82.1771, 64.9712, 46.3598, 31.5898, 30.1038, 25.8339, 23.9160]

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

