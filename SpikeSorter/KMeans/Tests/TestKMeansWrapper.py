# %%
# Importing the libraries
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from KMeansWrapper import KMeansWrapper

#%matplotlib qt

# %%
# Importing the dataset
filename = os.path.join(parentdir, "../datasets/16h_25m_26s.txt")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 3].to_numpy()

# %%
# Initialize global params
sampleRate = 10000
classfier = KMeansWrapper(model = parentdir + "/models/kmeans_large.pkl", sampleRate = sampleRate)

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
    classification = classfier.predict(extra[i])
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