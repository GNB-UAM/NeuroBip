# %%
# Importing the libraries
import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(os.path.dirname(parentdir))

import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import Model, models
from scipy.ndimage.interpolation import shift
from Utils.Normalizer import Normalizer

#%matplotlib qt
def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

def center_spike(window):
    return shift(window, (len(window)//2) - np.argmax(window), cval=0)

# %%
# Importing the dataset
filename = os.path.join(parentdir, "../datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

sampleRate = 10000

extra = dataset.iloc[:, 2].to_numpy()
extra = extra[:60*sampleRate]
pd = dataset.iloc[:, 3].to_numpy()

extra = normalize(extra, 5*1000)

plt.plot(extra[:5*sampleRate], label = 'extra')
plt.plot(pd[:5*sampleRate], label = 'pd')
plt.legend()
plt.show()

# %%
# Initialize global params
window_size = 20*10
features_dim = 32
input_dim = features_dim
num_classes = 4

print("Loading encoder...")

autoencoder = models.load_model(os.path.join(parentdir, 'models/encoder_lrelu_{}_{}.h5'.format(window_size, features_dim)))
encoder = Model(autoencoder.input, autoencoder.layers[-2].output)
perceptron = models.load_model(os.path.join(parentdir, 'models/perceptron_{}_{}.h5'.format(input_dim, num_classes)))

# %%
mapClassificationPerceptron = {'LP': ['red', 2], 'PY': ['blue', 0], 'PD': ['green', 1]}

# %%
# Classify
classif = np.array([])

print("Classifying...")

i = 0

while i + window_size < 30*sampleRate:
    if i % window_size == 0:
        window = np.array([extra[i:i+window_size],])
        classif = np.append(classif, np.argmax(perceptron.predict(encoder.predict(center_spike(window)))[0]))
    i += 1

plt.plot(classif, label = 'classif')
plt.show()

# %%
# Plot results
startPlot = 0
endPlot = 40*sampleRate
plt.figure()
plt.scatter(list(range(startPlot, endPlot)), extra[startPlot:endPlot], s=5, label="Perceptron Classifier")
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')

plt.show()