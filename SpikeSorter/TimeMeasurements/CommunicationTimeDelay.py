import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Importing the dataset
filename = os.path.join(os.path.dirname(__file__), "datasets/11h42m58s-15-Jun-2022.csv")
dataset = pd.read_csv(filename, delimiter=' ', header=None)

sampleRate = 10000

base = dataset.iloc[:, 2].to_numpy() - 0.5
robot = dataset.iloc[:, 1].to_numpy() - 0.5


plt.plot(base[:sampleRate], label = 'Base')
plt.plot(robot[:sampleRate], label = 'Robot')
plt.legend()
plt.show()


baseTimes = []
robotTimes = []
baseState = 1
robotState = 1
for index in range(len(base)):
    if baseState == 1:
        if base[index] < 0:
            baseState = 0
    else:
        if base[index] > 0:
            baseTimes.append(index)
            baseState = 1

    if robotState == 1:
        if robot[index] < 0:
            robotState = 0
    else:
        if robot[index] > 0:
            robotTimes.append(index)
            robotState = 1

deltaTimes = np.subtract(robotTimes, baseTimes) / sampleRate
print(np.std(deltaTimes)**2)
plt.hist(deltaTimes, weights=100*np.ones(len(deltaTimes)) / len(deltaTimes))
plt.title("Actuation delays distribution")
plt.xlabel("Delay (s)")
plt.ylabel("% of messages sent")
plt.show()

print(np.average(deltaTimes))
