class PID:

    def __init__(self, proportional, integral, derivative):
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative

    def save(self, gyroAngle, servoAngles, deltaTime):
        pass
