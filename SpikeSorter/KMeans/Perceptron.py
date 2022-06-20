import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import Model, models, Input, callbacks, activations, losses, layers, initializers
from Utils.Normalizer import Normalizer
from scipy.ndimage.interpolation import shift
from OldClassifier.OldClassifier import OldClassifier

FROM_DATA = True
GRAPHS = True

def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

def center_spike(window):
    return shift(window, (len(window)//2) - np.argmax(window), cval=0)

def noiseWindows(window):
    return np.amax(window) < 0.5

def mapLabel(classif, window):
    if noiseWindows(window):
        return 0
    elif classif == "LP":
        return 1
    elif classif == "PY":
        return 2
    elif classif == "PD":
        return 3

window_size = 20*10
sampleRate = 10000
features_dim = 32
input_dim = features_dim
num_classes = 4

if FROM_DATA:
    print("Loading data...")

    filename = os.path.join(parentdir, "datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")#15h42m45s-02-Mar-2022.dat")
    dataset = pd.read_csv(filename, delimiter=' ', header=2)
    extra = dataset.iloc[:, 2]
    pd = dataset.iloc[:, 3]

    print("Loading encoder...")

    autoencoder = models.load_model(os.path.join(currentdir, 'models/encoder_lrelu_{}_{}.h5'.format(window_size, features_dim)))
    encoder = Model(autoencoder.input, autoencoder.layers[-2].output)

    encoder.summary()
    input("Press Enter to continue...")

    print("Preprocessing data...")

    oldclassifier = OldClassifier(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2)

    extra = normalize(extra, 5*sampleRate)
    pd = normalize(pd, 5*sampleRate)

    features = np.array([])
    labels = np.array([])

    i = 0

    while i + window_size < len(extra):
        oldClass = oldclassifier.classify(extra[i], pd[i])

        if i % window_size == 0:
            window = np.array([extra[i:i+window_size],])
            #features = np.append(features, encoder.predict(center_spike(window))[0])
            labels = np.append(labels, mapLabel(oldClass, window))
        
        i += 1

    features = features.reshape((len(features) // input_dim, input_dim))

    #np.save(os.path.join(currentdir, 'features/features_lrelu_{}_{}.npy'.format(window_size, features_dim)), features)
    #np.save(os.path.join(currentdir, 'labels/labels_lrelu_{}_{}.npy'.format(window_size, features_dim)), labels)

    classif = []

    for i in range(len(labels)):
        if labels[i] == 0:
            classif.append(['yellow']*window_size)
        elif labels[i] == 1:
            classif.append(['green']*window_size)
        elif labels[i] == 2:
            classif.append(['red']*window_size)
        elif labels[i] == 3:
            classif.append(['blue']*window_size)
    
    classif = np.array(classif)
    classif = classif.flatten()
    startPlot = 0
    endPlot = 10*sampleRate
    plt.scatter(list(range(startPlot, endPlot)), extra[startPlot:endPlot], c=classif[startPlot:endPlot], s=5, label="Old Classifier Labels")
    plt.show()

else:
    print("Reading data...")
    features = np.load(os.path.join(currentdir, 'features/features_lrelu_{}_{}.npy'.format(window_size, features_dim)))
    labels = np.load(os.path.join(currentdir, 'labels/labels_lrelu_{}_{}.npy'.format(window_size, features_dim)))

features = extra[:-(len(extra) % window_size)]
features = features.reshape((len(features) // window_size, window_size))

print(features.shape)
print(labels.shape)

features_train = features[:int(len(features) * 0.8)]
features_test = features[int(len(features) * 0.8):]
labels_train = labels[:int(len(labels) * 0.8)]
labels_test = labels[int(len(labels) * 0.8):]

print("Shapes: {} {} {} {}".format(features_train.shape, features_test.shape, labels_train.shape, labels_test.shape))


print("Building model...")

perceptron = models.Sequential(name='Perceptron_{}_{}'.format(input_dim, num_classes))

perceptron.add(Input(shape=(200, ), name='input'))
perceptron.add(layers.Dense(units=100, kernel_initializer=initializers.GlorotUniform(seed=None),))
perceptron.add(layers.LeakyReLU(alpha=0.3))
perceptron.add(layers.Dense(units=50, kernel_initializer=initializers.GlorotUniform(seed=None),))
perceptron.add(layers.LeakyReLU(alpha=0.3))
perceptron.add(layers.Dense(num_classes, activation=activations.softmax, name='output'))

perceptron.summary()
input("Press Enter to continue...")

callback = callbacks.EarlyStopping(monitor='val_loss', mode='min', patience=100, restore_best_weights=True)

print("Compiling model...")

cross_entropy = losses.SparseCategoricalCrossentropy(
    from_logits=False, reduction=losses.Reduction.AUTO, name="sparse_categorical_crossentropy"
)

perceptron.compile(
    loss=cross_entropy,
    metrics=['sparse_categorical_crossentropy'],
    optimizer='adam'
)

print("Training model...")

history = perceptron.fit(
    features_train,
    labels_train,
    epochs=1000, 
    batch_size=128,
    validation_data=(features_test, labels_test),
    callbacks=[callback]
)

predictions = perceptron.predict(features_test)
predictions = predictions.argmax(axis=1)

print('Test accuracy: ',  np.mean(predictions == labels_test) * 100)

print("Saving model... {}_{}".format(input_dim, num_classes))

perceptron.save(os.path.join(currentdir, 'models/perceptron_{}_{}.h5'.format(input_dim, num_classes)))

if GRAPHS:
    print("Model metrics...")

    plt.figure()
    plt.title('Loss comparison on {} to {} Perceptron'.format(input_dim, num_classes))
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')

    plt.figure()
    plt.title('Sparse categorical crossentropy comparison on {} to {} Perceptron'.format(input_dim, num_classes))
    plt.plot(history.history['sparse_categorical_crossentropy'], label='train_mae')
    plt.plot(history.history['val_sparse_categorical_crossentropy'], label='test_mae')
    plt.xlabel('Epoch')
    plt.ylabel('Sparse categorical crossentropy')
    plt.legend(loc='upper right')

    plt.show()