import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32]
runtimes = [318.1381185054779, 187.9309117794037, 119.32512593269348, 78.9184422492981, 71.32934522628784, 76.90749216079712]
speedup = [40.74608302116394 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of MapReduce Twitter Job")
plt.grid()
plt.show()