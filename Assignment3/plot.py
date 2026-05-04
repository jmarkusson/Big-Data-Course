import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32]
runtimes = [40.74608302116394, 22.475059747695923, 16.742673873901367, 13.56257963180542, 10.931524276733398, 11.202193975448608]
speedup = [40.74608302116394 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of MapReduce Twitter Job")
plt.grid()
plt.show()