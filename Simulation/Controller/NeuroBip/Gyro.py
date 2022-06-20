from machine import ADC, Pin
from math import pi
from NeuroBip.Utils import map

class Gyro:

    def __init__(self, pinX, pinY, pinZ):
        self.adcs = [ADC(Pin(pinX, Pin.IN)), ADC(Pin(pinY, Pin.IN)), ADC(Pin(pinZ, Pin.IN))]
        for i in range(len(self.adcs)):
            self.adcs[i].atten(ADC.ATTN_11DB)

    def getAngles(self):
        angles = []
        for adc in self.adcs:
            angles.append(map(max(min(adc.read(), 7900), 2730), 2730, 7900, pi/2, -pi/2))
        return angles

    def getAngle(self, axis):
        return map(max(min(self.adcs[axis].read(), 7900), 2730), 2730, 7900, pi/2, -pi/2)
