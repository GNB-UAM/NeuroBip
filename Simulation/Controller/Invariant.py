from cmath import pi

class Invariant:
    def __init__(self, mapCicles):
        self.lastNeuron = 0
        self.LP_time = 0
        self.PY_time = 0
        self.PD_time = 0
        self.inv1Amplitude = pi
        self.inv2Amplitude = pi

        self.LP_end_time = 0

        self.mapCicles = mapCicles
        self.mapCiclesCounter = 0
        self.frequencyBase = 0
        self.amplitude1Base = 0
        self.amplitude2Base = 0

    def calculate(self, detectedNeuron, detectionTime):
        if detectedNeuron == self.lastNeuron:
            return None, None

        self.lastNeuron = detectedNeuron
        if detectedNeuron == 0:
            if self.LP_time < self.PY_time and self.PY_time < self.PD_time:
                period = (detectionTime - self.LP_time)
                inv1 = self.PD_time - self.LP_time
                inv2 = self.PD_time - self.PY_time
                amplitude1 = inv1 * self.inv1Amplitude / period
                amplitude2 = inv2 * self.inv2Amplitude / inv1

                self.LP_time = detectionTime

                if self.mapCiclesCounter < self.mapCicles:
                    self.frequencyBase += 1 / (period * self.mapCicles)
                    self.amplitude1Base += amplitude1 / self.mapCicles
                    self.amplitude2Base += amplitude2 / self.mapCicles
                    self.mapCiclesCounter += 1
                    return None, None

                return 1/(period*self.frequencyBase), [amplitude1/self.amplitude1Base, amplitude2/self.amplitude2Base, amplitude2/self.amplitude2Base]
            else:
                self.LP_time = detectionTime

        elif detectedNeuron == 1:
            # self.PY_time = detectionTime
            self.LP_end_time = detectionTime
        elif detectedNeuron == 2:
            self.PY_time = self.LP_end_time
            self.PD_time = detectionTime

        return None, None