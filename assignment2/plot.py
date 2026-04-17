import matplotlib.pyplot as plt

num_workers = [1, 2, 4, 8, 16, 32, 64]

speedups = [40.4101, 48.2563, 26.5371, 15.8294, 17.1842, 18.9233, 19.8408]

theoretical_speedup = 20.0

plt.plot(num_workers, speedups, marker='o', color='blue', linestyle='-', label="Measured speedup")

plt.axhline(y=theoretical_speedup, color='red', linestyle='--', label='Max Speedup (Amdahl\'s Law)')

plt.xlabel("Num workers")
plt.ylabel("Counting words times")
plt.title("Measuring parallization speeds by worker count")
plt.xticks(num_workers)