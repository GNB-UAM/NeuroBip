from RSLib.UnitTransform import *
from Box2D import b2_pi

class Servo:

    torque = 1.8 # kg*cm
    speed = 10.47 # rad / s
    absoluteLowerAngle = -b2_pi / 2
    absoluteUpperAngle = b2_pi / 2
    lowerAngle = absoluteLowerAngle
    upperAngle = absoluteUpperAngle
    angleSetted = 0

    def __init__(self, world, objectA, objectB, anchorA = None, anchorB = None, torqueCustom = None):

        self.objectA = objectA
        self.objectB = objectB
        self.anchorA = (0,0)
        self.anchorB = (0,0)

        if anchorA is not None:
            self.anchorA = anchorA
        if anchorB is not None:
            self.anchorB = anchorB
        if torqueCustom is not None:
            self.torque = torqueCustom
        
        self.world = world
        self.revolute = world.CreateRevoluteJoint(
            bodyA = self.objectA,
            bodyB = self.objectB,
            localAnchorA = self.anchorA,
            localAnchorB = self.anchorB,
            lowerAngle = self.lowerAngle,
            upperAngle = self.upperAngle,
            enableLimit = True,
            motorSpeed = self.speed,
            maxMotorTorque = torque(self.torque, "kg", "cm")*1000,
            enableMotor = True,
        )

    def getAngle(self):
        return self.revolute.angle

    def setAngle(self, angle):
        if angle < self.absoluteLowerAngle or angle > self.absoluteUpperAngle:
            return

        # Avoids jiggling
        if angle == self.angleSetted:
            self.revolute.SetLimits(angle, angle)
            return
        
        if angle < self.getAngle():
            self.revolute.SetLimits(angle, self.getAngle())
            self.revolute.motorSpeed = -self.speed
        elif angle > self.getAngle():
            self.revolute.SetLimits(self.getAngle(), angle)
            self.revolute.motorSpeed = self.speed

        self.angleSetted = angle

    def remove(self):
        self.world.DestroyJoint(self.revolute)
    
    def freeze(self):
        self.revolute.motorSpeed = 0
        self.revolute.enableMotor = False
        
        