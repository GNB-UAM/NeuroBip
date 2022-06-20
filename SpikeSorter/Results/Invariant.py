from cmath import pi

class Invariant:
    def __init__(self):
        self.lastNeuron = 0
        self.LP_time = 0
        self.PY_time = 0
        self.PD_time = 0

    def calculate(self, detectedNeuron, detectionTime):
        if detectedNeuron == self.lastNeuron:
            return None, None, None

        self.lastNeuron = detectedNeuron
        if detectedNeuron == 0:
            if self.LP_time < self.PY_time and self.PY_time < self.PD_time:
                period = (detectionTime - self.LP_time)
                inv1 = self.PD_time - self.LP_time
                inv2 = self.PD_time - self.PY_time
                self.LP_time = detectionTime
                return period, inv1, inv2
            else:
                self.LP_time = detectionTime

        elif detectedNeuron == 1:
            self.PY_time = detectionTime
        elif detectedNeuron == 2:
            self.PD_time = detectionTime

        return None, None, None