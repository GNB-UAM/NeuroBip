import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Utils.Normalizer import Normalizer
from ThreshClassifier.ThreshClassifier import ThreshClassifier

# Normalizer + ThreshClassifier
class ThreshClassifierWrapper:

    def __init__(self, thresholdLP = 4, thresholdPDLow = 0, thresholdPD = 1, sampleRate = 10000, maxCalibrateNormalization = 5):
        self.normalizerExtra = Normalizer()
        self.normalizerPD = Normalizer()
        self.threshClassifier = ThreshClassifier()
        self.maxCalibrateNormalization = int(maxCalibrateNormalization*sampleRate)
        self.lastClassification = 'LP'
        self.counter = 0

        self.thresholdLP = thresholdLP
        self.thresholdPD = thresholdPD
        self.thresholdPDLow = thresholdPDLow

    def predict(self, dataExtra, dataPD, normalized=False):
        if not normalized and self.counter < self.maxCalibrateNormalization:
            self.normalize(dataExtra, dataPD)
            return None
        
        if not normalized:
            # self.normalize(dataExtra, dataPD) # Keep adjusting the means and std in case there is drifting
            dataExtra = self.normalizerExtra.normalize(dataExtra)
            dataPD = self.normalizerPD.normalize(dataPD)
        
        
        '''
        stdExtra = self.normalizerExtra.getStd()
        meanExtra = self.normalizerExtra.getMean()
        stdPD = self.normalizerPD.getStd()
        meanPD = self.normalizerPD.getMean()

        thresholdLP = meanExtra +(self.thresholdLP * stdExtra)
        thresholdPD = meanPD +(self.thresholdPD * stdPD)
        thresholdPDLow = meanPD +(self.thresholdPDLow * stdPD)
        '''

        classification = self.threshClassifier.classify(dataExtra, dataPD, self.thresholdLP, self.thresholdPD, self.thresholdPDLow)
        
        if classification != self.lastClassification:
            self.lastClassification = classification
            return classification
        return None

    def normalize(self, dataExtra, dataPD):
        self.normalizerExtra.calibrate(dataExtra)
        self.normalizerPD.calibrate(dataPD)
        self.counter += 1