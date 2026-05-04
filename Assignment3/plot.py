import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32]
speedup = []

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of MapReduce Twitter Job")
plt.grid()
plt.show()