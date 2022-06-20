import matplotlib.pyplot as plt

file = open("Results/data/gaResults.txt", "r")

data = file.readlines()
data = [float(line.split()[-1]) for line in data]

plt.plot(data)
plt.title("Genetic Algorithm training from kinematic seed")
plt.legend(["Fitness"])
plt.xlabel("Generation")
plt.ylabel("Distance (cm)")
plt.show()
