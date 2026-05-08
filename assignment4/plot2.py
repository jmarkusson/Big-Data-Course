import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32,64]
runtimes = [100.28154754638672, 89.15495562553406, 58.53412342071533, 39.52981519699097, 29.8591787815094, 21.85932469367981, 19.17051362991333]
speedup = [100.28154754638672 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of Spark Twitter Followers Job")
plt.grid()
plt.show()