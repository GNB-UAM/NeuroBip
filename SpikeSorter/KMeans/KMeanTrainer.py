# %%
# Importing the libraries
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import tensorflow.keras as keras
from FeatureExtraction import *
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from Utils.Buffer import Buffer
from Utils.Normalizer import Normalizer
from Utils.BPFilter import BPFilter

#%matplotlib qt
GRAPHS = True

# %%
# Importing the dataset
filename = os.path.join(parentdir, "datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 2].to_numpy()
# %%
# Initialize global params
sampleRate = 10000

drop = 1
windowsWidth = int(20*10/drop)
circularBuffer = Buffer(windowsWidth, windowsWidth//2, drop)
normalizer = Normalizer()
autoencoder = keras.models.load_model(os.path.join(currentdir, 'models/encoder_{}_{}.h5'.format(200, 32)))
encoder = keras.Model(autoencoder.input, autoencoder.layers[-2].output)
# %%
# Train normalizer
trainData = extra[:sampleRate*5 if sampleRate*5 < len(extra) else len(extra)]

for data in trainData:
    normalizer.calibrate(data)
# %%
# Feature extraction
i = 0
features = np.array([])
features_dim = 32

for index, data in enumerate(extra[:]):
    windows = circularBuffer.add(data)
    if windows is not None:
        features = np.append(features, featureExtraction(np.array([normalizer.normalize(windows)])))

features = features.reshape((len(features) // 3, 3))

print("Features: " + str(features.shape))

# %%
# Feature plot
if GRAPHS:
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.scatter(features[:, 0], features[:, 1], features[:, 2])
    ax.set_xlabel("Energy")
    ax.set_ylabel("Amplitude")
    ax.set_zlabel("Frequency")
    plt.title('Feature Extraction')
    plt.show()

# %%
# Get # of clusters (3)
"""Nc = range(1, 10)
kmeans = [KMeans(n_clusters=i) for i in Nc]
kmeans
score = [kmeans[i].fit(features).score(features) for i in range(len(kmeans))]
score
plt.plot(Nc,score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()"""

# %%
# Fit clusters
k = 3
kmeans = KMeans(n_clusters = k).fit(features)
C = kmeans.cluster_centers_

## %%
# Infer by clusters
labels = kmeans.predict(features)

# %%
# Plot clusters
if GRAPHS:
    colors=['red','green', 'blue', 'yellow', 'purple']
    clusterColors=[]
    for row in labels:
        clusterColors.append(colors[row])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel("Energy")
    ax.set_ylabel("Amplitude")
    ax.set_zlabel("Mean Frequency")
    ax.scatter(features[:, 0], features[:, 1], features[:, 2], c=clusterColors, s=20)
    ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker='*', c='black', s=1000)

## %%
# Map clusters to extracelular activity
if GRAPHS:
    extraColours=[]

    for index, label in enumerate(labels):
        if index == 0 or index == len(labels)-1:
            extraColours.extend([colors[label]]*(windowsWidth//2))
        else:
            if windowsWidth//2 % 2 == 0:
                extraColours.extend([colors[label], colors[labels[index + 1]]]*(windowsWidth//4))
            else:
                extraColours.extend([colors[label], colors[labels[index + 1]]]*(windowsWidth//4))
                extraColours.append(colors[label])

    print(extra.shape, len(extraColours))

    ## %%
    # Plot extracelular activity clustered
    start = 7*10000
    endPlot = start + 5*10000
    #%matplotlib qt
    plt.figure()
    plt.scatter(list(range(start, endPlot)), extra[start:endPlot], c=extraColours[start:endPlot], s=5)
    plt.show()

# %%
# Store K-Means model and description
with open(os.path.join(os.path.dirname(__file__), "models/kmeans_half_description"), 'w') as f:
    f.write("num_features={},num_classes={},sampleRate={},windowsWidth={},LP={},PY={},PD={}".format(3, k, sampleRate/drop, windowsWidth, 0, 1, 2))

pickle.dump(kmeans, open(os.path.join(os.path.dirname(__file__), "models/kmeans_encoder_center.pkl"), "wb"))

# %%
