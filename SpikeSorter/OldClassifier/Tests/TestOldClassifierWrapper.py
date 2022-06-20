# %%
# Importing the libraries
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from OldClassifierWrapper import OldClassifierWrapper

#%matplotlib qt

# %%
# Importing the dataset
filename = os.path.join(parentdir, "../datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 2].to_numpy()
pd = dataset.iloc[:, 3].to_numpy()

# %%
# Initialize global params
sampleRate = 10000
classifier = OldClassifierWrapper(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2, sampleRate = sampleRate)

# %%
def mapClassification(classification):
    if classification == 'LP':
        return 'red'
    elif classification == 'PY':
        return 'green'
    elif classification == 'PD':
        return 'blue'
# %%
# Classify
classif = []
currenClassif = 'LP'

for i in range(len(extra)):
    classification = classifier.predict(extra[i], pd[i])
    if classification is not None:
        currenClassif = classification
    classif.append(mapClassification(currenClassif))

# %%
# Plot results
startPlot = 0
endPlot = 40*sampleRate
plt.scatter(list(range(startPlot, endPlot)), extra[startPlot:endPlot], c=classif[startPlot:endPlot], s=5, label="Original")
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')
plt.show()

# %%
times = []

for clas in classif:
    if clas == 'red':
        times.append(0)
    elif clas == 'green':
        times.append(1)
    elif clas == 'blue':
        times.append(2)
    
np.save("times.npy", times)