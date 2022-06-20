from machine import ADC, Pin, PWM
from math import pi
from NeuroBip.Utils import map

class Servo:

    def __init__(self, pinServo, pinRead=None, invert=False, offset=pi/2):
        self.servo = PWM(Pin(pinServo))
        self.servo.freq(400)
        self.invert = -1 if invert else 1
        self.adcServo = None
        self.offset = abs(offset)
        if pinRead is not None:
            self.adcServo = ADC(Pin(pinRead, Pin.IN))
            self.adcServo.atten(ADC.ATTN_11DB)
        
    def setAngle(self, angle):
        self.servo.duty(int(map(max(min(self.offset + self.invert*angle, pi), 0), 0, pi, 220, 1000)))

    def getAngle(self):
        return map(max(min(self.adcServo.read(), 8200), 1000), 1000, 8200, pi, 0) if self.adcServo is not None else -1
