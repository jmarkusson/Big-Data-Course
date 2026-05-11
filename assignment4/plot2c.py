import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32,64]
runtimes = [587.6, 584.4, 318.8, 172.3, 106.4, 66.7, 55.5]
speedup = [587.6 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of Spark Climate Job (Large Dataset)")
plt.grid()
plt.show()