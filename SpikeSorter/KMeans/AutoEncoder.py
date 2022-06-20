# [200 32] [32 8] [8 4] NO NEED TO TRAIN ON CENTERED SPIKE
import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import Input, initializers, callbacks
from tensorflow.keras.layers import LeakyReLU, Dense
from tensorflow.keras.models import Sequential
from Utils.Normalizer import Normalizer
from scipy.ndimage.interpolation import shift

GRAPHS = True
DATASET = True

input_dim = 200
features_dim = 32

def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

def center_spike(window):
    return window#shift(window, (len(window)//2) - np.argmax(window), cval=0)

print("Loading data...")
if DATASET:
    filename = os.path.join(parentdir, "datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")#15h42m45s-02-Mar-2022.dat")
    dataset = pd.read_csv(filename, delimiter=' ', header=2)
    extra = dataset.iloc[:, 2]
else:
    extra = np.load(os.path.join(currentdir, 'features/features_{}_{}.npy'.format(200, 32)))

print("Breaking data...")

if DATASET:
    extra = normalize(extra, 5*1000)

extra_train = extra[:int(len(extra) * 0.8)]
extra_test = extra[int(len(extra) * 0.8):]

if len(extra_train) % input_dim != 0:
    extra_train = extra_train[:-(len(extra_train) % input_dim)]
extra_train = extra_train.reshape((len(extra_train) // input_dim, input_dim))
extra_train_centered = np.array([center_spike(train) for train in extra_train])
print(extra_train_centered.shape)

if len(extra_test) % input_dim != 0:
    extra_test = extra_test[:-(len(extra_test) % input_dim)]
extra_test = extra_test.reshape((len(extra_test) // input_dim, input_dim))
extra_test_centered = np.array([center_spike(test) for test in extra_test])
print(extra_test_centered.shape)

if GRAPHS:
	plt.plot(extra[:5*10000])
	plt.show()

print("Building model...")

auto_encoder = Sequential(name='AutoEncoder_{}_{}'.format(input_dim, features_dim))

auto_encoder.add(Input(shape=(input_dim, ), name='input'))
auto_encoder.add(Dense(
    units=features_dim,
    kernel_initializer=initializers.GlorotUniform(seed=None),
    name='bottleneck'))
auto_encoder.add(LeakyReLU(alpha=0.3))
auto_encoder.add(Dense(
    units=input_dim,
    kernel_initializer=initializers.GlorotUniform(seed=None),
    name='output'))

auto_encoder.summary()
input("Press Enter to continue...")

callback = callbacks.EarlyStopping(monitor='val_loss', mode='min', patience=100, restore_best_weights=True)

print("Compiling model...")

auto_encoder.compile(
    loss='mae',
    metrics=['mae'],
    optimizer='adam'
)

print("Training model...")

history = auto_encoder.fit(
    extra_train_centered,
    extra_train_centered,
    epochs=10000, 
    batch_size=128,
    validation_data=(extra_test_centered, extra_test_centered),
    callbacks=[callback]
)

print("Saving model... {}_{}".format(input_dim, features_dim))

auto_encoder.save(os.path.join(currentdir, 'models/encoder_lrelu_{}_{}.h5'.format(input_dim, features_dim)))

if GRAPHS:
    print("Model metrics...")

    plt.figure()
    plt.title('Loss comparison on {} to {} Autoencoder'.format(input_dim, features_dim))
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')

    plt.figure()
    plt.title('MAE comparison on {} to {} Autoencoder'.format(input_dim, features_dim))
    plt.plot(history.history['mae'], label='train_mae')
    plt.plot(history.history['val_mae'], label='test_mae')
    plt.xlabel('Epoch')
    plt.ylabel('MAE')
    plt.legend(loc='upper right')

    plt.show()

if GRAPHS:
    print("Model predictions...")
    prediction = auto_encoder.predict(extra_train[:10]).flatten()
    plt.plot(extra_train.flatten()[:input_dim*10], label='original')
    plt.plot(prediction[:input_dim*10], label='prediction')
    plt.show()
