from NeuroBip.Servo import Servo
from NeuroBip.Gyro import Gyro
from NeuroBip.Communication import Communication
from Controller import Controller
from machine import Pin
from time import sleep
from KOscillator import KOscillators
from math import pi
import time

servos = [Servo(11, 7), Servo(9, 5, invert=True, offset=pi/2 - 30*pi/180), Servo(8, 4), Servo(10, 6, invert=True, offset=pi/2 - 5*pi/180)]
for servo in servos:
    servo.setAngle(0)
gyro = Gyro(1, 2, 3)
comm = Communication()
lights = [Pin(15, Pin.OUT), Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT)] # blue, red, green, white
maxAngle = 20*pi/180
genes = [0.4, 0.31303179479404734, -0.4082281750577982, -0.26993822831925085, -0.21149889395959587]
oscillators = KOscillators(
                3,
                [2*pi*genes[0], 4*pi*genes[0], 4*pi*genes[0]],
                [genes[1], genes[2]/2, genes[2]/2],
                X=[0, -genes[2]/2, -genes[2]/2],
                initialPhases = [0, genes[3], genes[4]],
                types=[0, 1, 1]
                )

controller = Controller(servos, gyro, comm, oscillators, lights)

prev_time = time.ticks_us()

while True:
    sleep(0.01)
    controller.update((time.ticks_us() - prev_time)/1000000)
    prev_time = time.ticks_us()