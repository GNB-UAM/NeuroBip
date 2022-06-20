import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(os.path.dirname(parentdir))

from OldClassifier.OldClassifierWrapper import OldClassifierWrapper
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import pandas as pd
from Utils.Normalizer import Normalizer
from sklearn.manifold import TSNE
from scipy.ndimage.interpolation import shift

SAVE_FEATURES = False

def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

def center_spike(window):
    return shift(window, (len(window)//2) - np.argmax(window), cval=0)

print("Loading data...")
filename = os.path.join(parentdir, "../datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")#15h42m45s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 2]
pd = dataset.iloc[:, 3]

extra = normalize(extra, 5*1000)
pd = normalize(pd, 5*1000)

plt.plot(extra[:5*10000])
plt.show()
plt.plot(pd[:5*10000])
plt.show()

print("Loading model...")
input_dim = 20*10
features_dim = 32
autoencoder = keras.models.load_model(os.path.join(parentdir, 'models/encoder_lrelu_{}_{}.h5'.format(input_dim, features_dim)))
encoder = keras.Model(autoencoder.input, autoencoder.layers[-2].output)

autoencoder.summary()
encoder.summary()

print("Predicting...")

def toColor(classif):
    if classif == "LP":
        return "red"
    elif classif == "PY":
        return "green"
    elif classif == "PD":
        return "blue"
    else:
        return "black"

sampleRate = 10000
oldClassifier = OldClassifierWrapper(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2, sampleRate = sampleRate)
predictions = np.array([])
features = np.array([])
total = 100
lastClassif = 0
labels = []

for i in range(total):
    for j in range(input_dim):
        classif = oldClassifier.predict(extra[i*input_dim + j], pd[i*input_dim + j], normalized=True)
        if classif is not None:
            lastClassif = classif
    labels.append(toColor(lastClassif))
    predictions = np.append(predictions, autoencoder.predict(center_spike(np.array([extra[i*input_dim:(i + 1)*input_dim],])))[0])
    features = np.append(features, encoder.predict(center_spike(np.array([extra[i*input_dim:(i + 1)*input_dim],])))[0])

features = features.reshape((len(features) // features_dim, features_dim))

plt.figure()
plt.plot(extra[:total*input_dim], label='original')
plt.plot(predictions, label='prediction')
plt.legend(loc='upper right')
plt.show()

print(features.shape)
features_embedded = TSNE(n_components=2, learning_rate='auto', init='random').fit_transform(features)

plt.scatter(features_embedded[:, 0], features_embedded[:, 1], s=5, c=labels)
plt.show()

if SAVE_FEATURES:
    print("Saving features...")

    if len(extra) % input_dim != 0:
        extra = extra[:-(len(extra) % input_dim)]
    extra = extra.reshape((len(extra) // input_dim, input_dim))

    features = encoder.predict(extra).flatten()
    print(features.shape)
    np.save(os.path.join(parentdir, 'features/features_{}_{}.npy'.format(input_dim, features_dim)), features)