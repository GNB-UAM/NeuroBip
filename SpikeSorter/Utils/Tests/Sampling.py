import pandas as pd
import matplotlib.pyplot as plt
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Importing the dataset
filename = os.path.join(parentdir, "../datasets/16h_25m_26s.txt")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 3].to_numpy()
pd = dataset.iloc[:, 2].to_numpy()

sampleRate = 10000
sampleDrop = 2

extraDropped = []

for i in range(len(extra)):
    if i % sampleDrop == 0:
        extraDropped.append(extra[i])
    else:
        extraDropped.append(extraDropped[-1])

def mse(sample1, sample2):
    return sum([(sample1[i] - sample2[i])**2 for i in range(len(sample1))])

startPlot = 0
endPlot = 5*sampleRate

plt.plot(extra[startPlot:endPlot],label="Original")
plt.plot(extraDropped[startPlot:endPlot],label="Simplified")
plt.title("Samplping drop of {} %, MSE: {}".format(100 - 100/sampleDrop, mse(extra, extraDropped)))
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')
plt.show()