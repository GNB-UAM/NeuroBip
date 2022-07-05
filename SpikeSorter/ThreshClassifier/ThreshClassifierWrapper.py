import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Utils.Normalizer import Normalizer
from ThreshClassifier.ThreshClassifier import ThreshClassifier

# Normalizer + ThreshClassifier
class OldClasThreshierWrapper:

    def __init__(self, thresholdLP = 4, LPresistance = 60*10, thresholdPD = 1, sampleRate = 10000, maxCalibrateNormalization = 5):
        self.normalizerExtra = Normalizer()
        self.normalizerPD = Normalizer()
        self.threshClassifier = ThreshClassifier(thresholdLP = thresholdLP, LPresistance = LPresistance, thresholdPD = thresholdPD)
        self.maxCalibrateNormalization = int(maxCalibrateNormalization*sampleRate)
        self.lastClassification = 'LP'
        self.counter = 0

    def predict(self, dataExtra, dataPD, normalized=False):
        if not normalized and self.counter < self.maxCalibrateNormalization:
            self.normalize(dataExtra, dataPD)
            return None
        
        if not normalized:
            dataExtra = self.normalizerExtra.normalize(dataExtra)
            dataPD = self.normalizerPD.normalize(dataPD)
        
        classification = self.threshClassifier.classify(dataExtra, dataPD)
        
        if classification != self.lastClassification:
            self.lastClassification = classification
            return classification
        return None

    def normalize(self, dataExtra, dataPD):
        self.normalizerExtra.calibrate(dataExtra)
        self.normalizerPD.calibrate(dataPD)
        self.counter += 1