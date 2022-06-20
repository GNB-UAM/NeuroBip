import matplotlib.pyplot as plt
import os
currentdir = os.path.dirname(os.path.realpath(__file__))

servoAngles = []
with open(os.path.join(os.path.dirname(__file__), "../datasets/servoAngles.txt")) as file:
    for line in file: 
        line = line.strip()
        servoAngles.append(float(line))

readAngles = []
with open(os.path.join(os.path.dirname(__file__), "../datasets/readAngles.txt")) as file:
    for line in file: 
        line = line.strip()
        readAngles.append(float(line) - 1.3)

plt.plot(servoAngles)
plt.plot(readAngles)
plt.show()