import numpy as np

class Normalizer:

    def __init__(self):
        self.oldMeans = 0
        self.newMeans = 0
        self.oldStds = 0
        self.newStds = 0
        self.elapsedCalibration = 1
    
    def calibrate(self, data):
        if self.elapsedCalibration == 1:
            self.oldMeans = self.newMeans = data
            self.oldStds = 0.0
        else:
            self.newMeans = self.oldMeans + (data - self.oldMeans) / self.elapsedCalibration
            self.newStds = self.oldStds + (data - self.oldMeans) * (data - self.newMeans)

            # set up for next iteration
            self.oldMeans = self.newMeans
            self.oldStds = self.newStds
        
        self.elapsedCalibration += 1

    def getMean(self):
        return self.newMeans

    def getStd(self):
        std = np.sqrt(self.newStds / (self.elapsedCalibration - 1))
        return std if std > 0.0 else 1.0

    def normalize(self, data):
        return (data - self.getMean()) / self.getStd()