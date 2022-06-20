import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from BPFilter import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

# Sample rate and desired cutoff frequencies (in Hz).
fs = 10000.0
lowcut = 50.0
highcut = 440.0

# Plot the frequency response for a few different orders.
plt.figure(1)
plt.clf()
for order in [1, 3, 5, 6]:
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    w, h = freqz(b, a, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
            '--', label='sqrt(0.5)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')

# Filter a noisy signal.
T = 0.05
nsamples = int(T * fs)
t = np.linspace(0, T, nsamples, endpoint=False)

centralFreq = (lowcut + highcut) / 2
x = 2 * np.sin(2 * np.pi * lowcut * t)
x += 1.5 * np.cos(2 * np.pi * highcut * t)
x += np.cos(2 * np.pi * centralFreq * t)

plt.figure(2)
plt.clf()
plt.plot(t, x, label='Noisy signal')

bpFilter = BPFilter(lowcut, highcut, fs, order = 5)
y = []
for data in x:
    y.append(bpFilter.filter(data))
plt.plot(t, y, label='Filtered signal (%g Hz)' % centralFreq)
plt.xlabel('time (seconds)')
plt.hlines([-1, 1], 0, T, linestyles='--')
plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')

plt.show()