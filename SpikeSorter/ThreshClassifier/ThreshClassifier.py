import numpy as np

class ThreshClassifier:

    # 3
    def __init__(self, thresholdLP, LPresistance, thresholdPD):
        self.state = 'LP'

        self.thresholdLP = thresholdLP
        self.LPresistance = LPresistance
        self.LPcurrentResistance = 0

        self.thresholdPD = thresholdPD

    def classify(self, dataExtra, dataPD):
        if self.state == 'LP':
            if dataExtra < self.thresholdLP:
                self.LPcurrentResistance += 1
            else:
                self.LPcurrentResistance = 0

            if self.LPcurrentResistance == self.LPresistance:
                self.state = 'PY'

        elif self.state == 'PY':
            if dataPD > self.thresholdPD:
                self.state = 'PD'
        
        elif self.state == 'PD':
            if dataExtra > self.thresholdLP:
                self.state = 'LP'

        return self.state
            