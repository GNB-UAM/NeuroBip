import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Importing the dataset
filename = os.path.join(os.path.dirname(__file__), "datasets/pycomediTimes.csv")
dataset = pd.read_csv(filename, delimiter=' ', header=None)

sampleRate = 10000

base = dataset.iloc[:, 2].to_numpy()
comedi = dataset.iloc[:, 1].to_numpy()


plt.plot(base[:sampleRate], label = 'Base')
plt.plot(comedi[:sampleRate], label = 'Comedi')
plt.legend()
plt.show()


baseTimes = []
comediTimes = []
baseState = 1
comediState = 1
for index in range(len(base)):
    if baseState == 1:
        if base[index] < 0:
            baseTimes.append(index)
            baseState = 0
    else:
        if base[index] > 0:
            baseTimes.append(index)
            baseState = 1

    if comediState == 1:
        if comedi[index] < 0:
            comediTimes.append(index)
            comediState = 0
    else:
        if comedi[index] > 0:
            comediTimes.append(index)
            comediState = 1

deltaTimes = np.subtract(comediTimes, baseTimes)
plt.hist(deltaTimes, weights=100*np.ones(len(deltaTimes)) / len(deltaTimes))
plt.title("Samples delay distribution at 10kHz")
plt.xlabel("Samples delayed")
plt.ylabel("% of total measures")
plt.show()

print(np.average(deltaTimes))
