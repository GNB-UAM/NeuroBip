import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(os.path.dirname(parentdir))

import matplotlib.pyplot as plt
import tensorflow.keras as keras
import pandas as pd
from Utils.Normalizer import Normalizer
from scipy.ndimage.interpolation import shift
from matplotlib.ticker import FuncFormatter

def alignment(vectA, vectB):
    return np.dot(vectA, vectB) / (np.linalg.norm(vectA) * np.linalg.norm(vectB))

def distance(vectA, vectB):
    return np.linalg.norm(vectA - vectB)

def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

def center_spike(window):
    return window#shift(window, (len(window)//2) - np.argmax(window), cval=0)
    
print("Loading data...")
filename = os.path.join(parentdir, "../datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")#15h42m45s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)
extra = dataset.iloc[:, 2]
extra = normalize(extra, 5*1000)
extra = extra[2550:2850]

fig, ax = plt.subplots()
plt.plot(extra)
plt.title("Strided Spike")
plt.ylabel("Normalized Waveform")
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{0:g}'.format(x/10)))
plt.xlabel("Time (ms)")
plt.show()

print("Loading model...")
input_dim = 20*10
features_dim = 32

autoencoder = keras.models.load_model(os.path.join(parentdir, 'models/encoder_lrelu_{}_{}.h5'.format(input_dim, features_dim)))
encoder = keras.Model(autoencoder.input, autoencoder.layers[-2].output)

print("Predicting...")
features = np.array([])

i = 0
while i + 200 < len(extra):
    features = np.append(features, encoder.predict(center_spike(np.array([extra[i:i+200],])))[0])
    i += 1

features = features.reshape((len(features) // features_dim, features_dim))
print(features.shape)

max_distance = 0
min_alignment = 1

i = 0
while i < len(features) - 1:
    align = alignment(features[i], features[i+1])
    dist = distance(features[i], features[i+1])
    if align < min_alignment:
        min_alignment = align
    if dist > max_distance:
        max_distance = dist
    i += 1

print("Max distance: {}".format(max_distance))
print("Min alignment: {}".format(min_alignment))

alignment_edges = alignment(features[0], features[-1])
distance_edges = distance(features[0], features[-1])

print("Alignment edges: {}".format(alignment_edges))
print("Distance edges: {}".format(distance_edges))

fig, ax = plt.subplots(1, 2)
fig.suptitle("Alignment edges centered spike: {}\nDistance: {}".format(alignment_edges, distance_edges))
plt.setp(ax, xlabel="Time (ms)", ylabel="Normalized Waveform")
ax[0].plot(extra[:200])
ax[1].plot(extra[-200:])
[ax[i].xaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{0:g}'.format(x/10))) for i in range(2)]
plt.show()