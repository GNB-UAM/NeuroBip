import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from KOscillator import KOscillators
from math import pi
import matplotlib.pyplot as plt

freq = 1
amp1 = pi/2
amp2 = pi/2
phase1 = 0
phase2 = 0

oscillators = KOscillators(
                3,
                [2*pi*freq, 4*pi*freq, 4*pi*freq],
                [amp1, amp2/2, amp2/2],
                X=[0, -amp2/2, -amp2/2],
                initialPhases = [0, -pi/2, -pi/2],
                types=[0, 1, 1]
                )

o1 = []
o2 = []
o3 = []

for i in range(1000):
    """
    if i == 200:
        oscillators.setAmplitude(0, pi/3)
    elif i == 400:
        oscillators.setAmplitude(1, pi/2)
    elif i == 600:
        oscillators.setAmplitude(0, pi/3)
    """
        
    output = oscillators.getNext(0.01)
    o1.append(output[0])
    o2.append(output[1])
    o3.append(output[2])

plt.plot(o1, label='Oscillator 1')
plt.plot(o2, label='Oscillator 2')
plt.plot(o3, label='Oscillator 3')
plt.legend()
plt.show()