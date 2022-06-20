from math import pi
import matplotlib.pyplot as plt
from Oscillator import Oscillator

o = Oscillator(5, 0, 0)
o.update(5, -pi/2, 0, 2*pi)
out = []

for i in range(0, 500):
    out.append(o.getNext(0.01)*180/pi)

plt.plot(out)
plt.show()