from math import pi
from PID import PID
from Invariant import Invariant

class Controller:
    def __init__(self, servos, gyro, communication, oscillators, lights = None):
        self.criticalAngle = 45*pi/180
        self.minAngle = -20*pi/180
        self.maxAngle = 20*pi/180
        self.servos = servos
        self.gyro = gyro
        self.communication = communication
        self.invariant = Invariant(10)

        # Base resonance frequencies and phases
        self.oscillators = oscillators
        self.pid = PID(2, 0.5, 0.2)
        self.servoAngles = [None] * (len(servos))
        self.gyroAngle = None

        self.detectedNeuron = 0
        self.detectionTime = 0

        self.lights = lights
        self.lightOn = 0
        if self.lights is not None:
            for light in self.lights:
                light.off()
        
        self.nextAngles = [0]*self.oscillators.numOscillators()
    
    def update(self, deltaTime):
        received = self.communication.receive()
        if received is not None:
            self.detectedNeuron = received[0]
            self.detectionTime = received[1]
            frequencyMultiple, amplitudeMultiples = self.invariant.calculate(self.detectedNeuron, self.detectionTime)
            if frequencyMultiple is not None and amplitudeMultiples is not None:
                pass#print("Invariants: f={}, amps={}".format(frequencyMultiple, amplitudeMultiples))
            self.updateOscillators(frequencyMultiple, amplitudeMultiples)
        
        self.gyroAngle = self.gyro.getAngle(1)

        for index, servo in enumerate(self.servos):
            self.servoAngles[index] = servo.getAngle()

        self.communication.send(self.gyroAngle, self.servoAngles)
        self.setOscillatorsAngles(self.servoAngles)

        if abs(self.gyroAngle) <= self.criticalAngle:
            self.updateLights(self.detectedNeuron)
            self.nextAngles = self.getOscillatorsNextAngles(deltaTime)
            self.setServosAngles(self.nextAngles)
        else:
            self.updateLights(-1)
            pidAngles = self.pid.save(self.gyroAngle, self.servoAngles, deltaTime)
            """
            self.setServosAngles(pidAngles)
            """

    def updateLights(self, neuron):
        if self.lights is not None and self.lightOn != neuron:
            self.lights[self.lightOn].off()
            self.lights[neuron].on()
            self.lightOn = neuron

    def updateOscillators(self, frequencyMultiple, amplitudeMultiples):
        if frequencyMultiple is not None and amplitudeMultiples is not None:
            self.oscillators.setFrequencyMultiple(frequencyMultiple)
            for index in range(self.oscillators.numOscillators()):
                self.oscillators.setAmplitudeMultiple(index, amplitudeMultiples[index])

    def setOscillatorsAngles(self, angles):
        oscillationTargetAngles = [angles[0]] + angles[2:]
        for index in range(self.oscillators.numOscillators()):
            if abs(self.nextAngles[index] - oscillationTargetAngles[index]) > 0.17: # 0.17 radians = 10 degrees
                pass#self.oscillators.setAngle(index, oscillationTargetAngles[index])
            

    def getOscillatorsNextAngles(self, deltaTime):
        nextAngles = self.oscillators.getNext(deltaTime)
        return [nextAngles[0], -nextAngles[0]] + nextAngles[1:]

    def setServosAngles(self, angles):
        for index, servo in enumerate(self.servos):
            servo.setAngle(angles[index])