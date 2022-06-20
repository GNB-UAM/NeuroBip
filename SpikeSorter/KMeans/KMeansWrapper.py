import pickle
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Utils.Normalizer import Normalizer
from Utils.Buffer import Buffer
from KMeans.FeatureExtraction import featureExtraction
from threading import Thread
import tensorflow.keras as keras
import numpy as np

# Normalizer + Buffer + KMeansClassifier
class KMeansWrapper:

    def __init__(self, model = "/models/kmeans_large.pkl", featureEx = featureExtraction, windowsWidth = 2.5*20*10, sampleRate = 10000, maxCalibrateNormalization = 5):
        self.ONLINE = False
        self.normalizer = Normalizer()
        drop = 1
        self.buffer = Buffer(int(windowsWidth/drop), int(windowsWidth/(drop*2)), drop)
        self.kmeans = pickle.load(open(model, "rb"))
        autoencoder = keras.models.load_model(os.path.join(currentdir, 'models/encoder_{}_{}.h5'.format(200, 32)))
        encoder = keras.Model(autoencoder.input, autoencoder.layers[-2].output)
        self.featureEx = featureExtraction#encoder.predict
        self.maxCalibrateNormalization = int(maxCalibrateNormalization*sampleRate)
        self.lastClassification = 0
        self.counter = 0
        if self.ONLINE:
            self.resultThread = None
            self.thread = None
            self.totalWindows = 0
            self.lostWindows = 0

    def predict(self, dataExtra):
        if self.counter < self.maxCalibrateNormalization:
            self.normalizer.calibrate(dataExtra)
            self.counter += 1
            return None

        window = self.buffer.add(self.normalizer.normalize(dataExtra))

        if self.ONLINE:
            return self.onlineClassification(window)

        return self.offlineClassification(window)

    def mapClassification(self, classification):
        if classification == 0:
            return 'LP'
        elif classification == 1:
            return 'PY'
        elif classification == 2:
            return 'PD'

    def onlineClassification(self, window):
        result = None
        if self.thread is not None and not self.thread.is_alive():
            self.thread.join()
            self.thread = None
            classification = self.resultThread
            if classification != self.lastClassification:
                self.lastClassification = classification
                result = self.mapClassification(classification)
        
        if window is not None:
            self.totalWindows += 1
            if self.thread is None:
                self.thread = Thread(target = self.predictThreadWrapper, args = ([window]))
                self.thread.start()
            else:
                self.lostWindows += 1
                print("Windows missed due to race condition")

        return result

    def offlineClassification(self, window):
        if window is not None:
            features = self.featureEx(np.array([window]))
            classification = self.kmeans.predict([features])#.astype(float))
            return self.mapClassification(classification)
        else:
            return None
        
    def predictThreadWrapper(self, window):
        self.resultThread = self.kmeans.predict(self.featureEx(np.array([window])))