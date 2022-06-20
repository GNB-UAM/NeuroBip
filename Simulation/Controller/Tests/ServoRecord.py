import time
import math

servo = Servo(10, 6)

servoAngles = []
readAngles = []

for i in range(0, 1000):
    servoAngles.append(math.pi*math.sin(i*0.1)/4)
    servo.setAngle(servoAngles[-1])
    time.sleep(0.01)
    readAngles.append(servo.getAngle())

with open('servoAngles.txt', 'w') as f:
    for item in servoAngles:
        f.write("%s\n" % item)

with open('readAngles.txt', 'w') as f:
    for item in readAngles:
        f.write("%s\n" % item)