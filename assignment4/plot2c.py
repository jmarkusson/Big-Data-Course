import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32,64]
runtimes = [X, Y, 1103.2, 593.8, 323.7, 198.9, 125.9]
speedup = [100.28154754638672 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of Spark Climate Job")
plt.grid()
plt.show()