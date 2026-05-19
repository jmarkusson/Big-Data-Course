import matplotlib.pyplot as plt
# Speedup plot for 3b


cores = [1,2,4,8,16,32,64]
runtimes = [604.54407, 623.65594, 389.87425, 243.38509, 113.38415, 82.32559, 56.01230]
speedup = [604.54407 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of Spark HyperLogLog Job")
plt.grid()
plt.show()