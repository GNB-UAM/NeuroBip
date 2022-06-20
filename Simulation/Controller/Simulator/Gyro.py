class Gyro:

    def __init__(self, neuroBip):
        self.neuroBip = neuroBip

    def getAngle(self, index):
        return self.neuroBip.angle
