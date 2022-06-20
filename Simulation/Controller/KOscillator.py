from math import pi, sin

class KOscillators:
    def __init__(self, N, w, R, X = None, couplingWeights = [[0, 0, 0], [0.5, 0, 0], [0.5, 0, 0]], initialPhases = [0, 0, 0], types = [0, 0, 0]):
        self.N = N
        self.originalFreqs = [x / (2*pi) for x in w]
        self.tW = w
        self.originalAmplitudes = [x for x in R]
        self.tR = R
        self.tX = X if X is not None else [0] * self.N
        self.sA = [0] * self.N
        self.sr = [0] * self.N
        self.sx = [0] * self.N
        self.sr_d = [0] * self.N
        self.sx_d = [0] * self.N
        self.couplingWeights = couplingWeights
        self.phaseBiases = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.initialPhases = initialPhases
        self.ar = self.ax = 2*pi
        self.types = types

    def numOscillators(self):
        return self.N
    
    def setFrequency(self, index, frequency):
        self.tW[index] = 2*pi*frequency

    def setFrequencyMultiple(self, frequencyMultiple):
        for index in range(self.N):
            self.setFrequency(index, self.originalFreqs[index] * frequencyMultiple)

    def setAmplitude(self, oscillator, amplitude):
        # Fixed max for knees type 1
        if self.types[oscillator] == 1:
            self.setOffset(oscillator, self.getAmplitude(oscillator) + self.getOffset(oscillator) - amplitude)
        
        self.tR[oscillator] = amplitude

    def setAmplitudeMultiple(self, oscillator, amplitudeMultiple):
        self.setAmplitude(oscillator, amplitudeMultiple * self.originalAmplitudes[oscillator])

    def setOffset(self, oscillator, offset):
        self.tX[oscillator] = offset

    def setAngle(self, oscillator, angle):
        self.sA[oscillator] = angle

    def setPhase(self, oscillator, phase):
        self.phaseBiases[oscillator][0] = phase

    def getAmplitude(self, oscillator):
        return self.tR[oscillator]

    def getOffset(self, oscillator):
        return self.tX[oscillator]
    
    def getNext(self, deltaTime):
        output = [0] * self.N
        new_sA = [0] * self.N
        new_sr = [0] * self.N
        new_sx = [0] * self.N
        new_sr_d = [0] * self.N
        new_sx_d = [0] * self.N

        for i in range(self.N):
            sA_d = self.tW[i]
            for j in range(self.N):
                sA_d += self.couplingWeights[i][j] * self.sr[j] * sin(self.sA[j] - self.sA[i] - self.phaseBiases[i][j])
            new_sA[i] = self.sA[i] + deltaTime * sA_d

            sr_dd = self.ar * ((self.ar / 4) * (self.tR[i] - self.sr[i]) - self.sr_d[i])
            new_sr_d[i] = self.sr_d[i] + deltaTime * sr_dd
            new_sr[i] = self.sr[i] + deltaTime * self.sr_d[i]

            sx_dd = self.ax * ((self.ax / 4) * (self.tX[i] - self.sx[i]) - self.sx_d[i])
            new_sx_d[i] = self.sx_d[i] + deltaTime * sx_dd
            new_sx[i] = self.sx[i] + deltaTime * self.sx_d[i]

        for i in range(self.N):
            self.sA[i] = new_sA[i]
            self.sr[i] = new_sr[i]
            self.sx[i] = new_sx[i]
            self.sr_d[i] = new_sr_d[i]
            self.sx_d[i] = new_sx_d[i]
            output[i] = self.sx[i] + self.sr[i] * sin(self.sA[i] + self.initialPhases[i])

        return output
