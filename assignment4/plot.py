import matplotlib.pyplot as plt
# Spedup plot for 3c


cores = [1,2,4,8,16,32,64]
runtimes = [26.48592209815979, 25.964308500289917, 22.405232667922974, 19.464842319488525, 18.6635684967041, 18.555287837982178, 14.646706581115723]
speedup = [26.48592209815979 / runtime for runtime in runtimes]

plt.plot(cores, speedup, marker='o')
plt.xlabel("Number of cores")
plt.ylabel("Speedup")
plt.title("Scalability of Spark Twitter Follows Job")
plt.grid()
plt.show()