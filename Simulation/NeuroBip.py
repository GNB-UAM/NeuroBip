from math import inf, pi
from Box2D import (b2Filter, b2FixtureDef, b2PolygonShape)
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Controller"))
from RSLib.UnitTransform import *
from Controller.Simulator.Servo import *
from NeuroBipParts import *
from Controller.Controller import Controller
from Controller.Simulator.Gyro import Gyro
from Controller.Simulator.Communication import Communication
from Controller.KOscillator import KOscillators
import struct
import time

class NeuroBip:

    LIMIT_ANGLE = pi/4

    def __init__(self, world, id, freq, amp1, amp2, phase1, phase2, port=None, offset = (0, 0)):
        self.id = id
        self.world = world
        self.offsetX, self.offsetY = offset
        self.neuroBip = self.createNeuroBip()
        self.maxAngle = 20*pi/180
        self.maxDistance = 0
        self.bornTime = time.time()
        self.params = [abs(freq), abs(amp1), amp2, phase1, phase2]
        self.port = port
        self.communication = Communication(port=port)
        self.controller = Controller(
            self.servos, Gyro(self.neuroBip[0]),
            self.communication,
            KOscillators(
                3,
                [2*pi*self.params[0], 4*pi*self.params[0], 4*pi*self.params[0]],
                [self.params[1], self.params[2]/2, self.params[2]/2],
                X=[0, -self.params[2]/2, -self.params[2]/2],
                initialPhases = [0, self.params[3], self.params[2]],
                types=[0, 1, 1]
                )
            )
        self.dead = False

    def getNeuroBip(self):
        return self.neuroBip

    def getParams(self):
        return self.params
    
    def createNeuroBip(self):
        
        leftFoot = self.createPart(NBFoot)
        leftFemur = self.createPart(NBFemur)
        leftKnee = Servo(self.world, leftFemur, leftFoot, anchorA = coordinate((10.5, 10.7), "mm"), anchorB = coordinate((13.3, 60.2), "mm"))

        rightFoot = self.createPart(NBFoot)
        rightFemur = self.createPart(NBFemur)
        rightKnee = Servo(self.world, rightFemur, rightFoot, anchorA = coordinate((10.5, 10.7), "mm"), anchorB = coordinate((13.3, 60.2), "mm"))
        
        hips = self.createPart(NBHips)
        hipLeft = Servo(self.world, hips, leftFemur, anchorA = coordinate((25.7, 10.7), "mm"), anchorB = coordinate((10.5, 70), "mm"))
        hipRight = Servo(self.world, hips, rightFemur, anchorA = coordinate((25.7, 10.7), "mm"), anchorB = coordinate((10.5, 70), "mm"))

        self.servos = [hipLeft, hipRight, leftKnee, rightKnee]

        return hips, rightFemur, leftFemur, rightFoot, leftFoot
    
    def createPart(self, description):
        fixtures = []
        for _, value in description.items():
            fixtures.append(
                b2FixtureDef(
                    shape = b2PolygonShape(vertices=vertices(value["coords"], "mm")),
                    density = densityFromMass(value["weight"], value["coords"], "g", "mm"),
                    friction = 1,
                    filter = b2Filter(
                        groupIndex = value["noCollideGroup"]
                    )
                )
            )

        return self.world.CreateDynamicBody(
            position = (self.offsetX, self.offsetY),
            fixtures = fixtures
        )

    def update(self, deltaTime):
        if self.dead:
            return
        self.controller.update(deltaTime)
        #for index, servo in enumerate(self.servos):
        #    servo.setAngle(self.oscillators[index].getNext(deltaTime))
    
    def sendMessage(self, message):
        oscillator, period, minAngle, maxAngle, phase = struct.unpack("!Hffff", message)
        #self.oscillators[oscillator].update(period, minAngle, maxAngle, phase)

    def getPosition(self):
        return self.neuroBip[0].position

    def getStatus(self):
        return self.neuroBip[0].position, self[0].neuroBip.angle

    def freeze(self):
        for servo in self.servos:
            servo.freeze()

    def remove(self):
        if self.dead:
            return
        self.maxDistance = self.neuroBip[0].position.x
        self.livingTime = time.time() - self.bornTime
        for part in reversed(self.neuroBip):
            self.world.DestroyBody(part)

    def checkDead(self):
        if not self.dead and abs(self.neuroBip[0].angle) >= self.LIMIT_ANGLE:
            self.freeze()
            self.remove()
            self.dead = True
            return True
        return self.dead