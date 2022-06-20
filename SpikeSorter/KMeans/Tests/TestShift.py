import numpy as np
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(os.path.dirname(parentdir))

import matplotlib.pyplot as plt
import pandas as pd
from Utils.Normalizer import Normalizer
from scipy.ndimage.interpolation import shift
from matplotlib.ticker import FuncFormatter

def shift_spike(window):
    return shift(window, (len(window)//2) - np.argmax(window), cval=0)

def normalize(data, calibrationPoints):
    normalizer = Normalizer()
    for i in range(calibrationPoints):
        normalizer.calibrate(data[i])
    
    return np.array([normalizer.normalize(dataPoint) for dataPoint in data])

print("Loading data...")
filename = os.path.join(parentdir, "../datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")#15h42m45s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)
extra = dataset.iloc[:, 2]
extra = normalize(extra, 5*1000)
extra = extra[740:1100]

fig, ax = plt.subplots(2, 2)
fig.suptitle("Centered Spike")
plt.setp(ax, xlabel="Time (ms)", ylabel="Normalized Waveform")
ax[0,0].plot(extra[:200])
ax[0,0].set_title("Original")
ax[0,1].plot(shift_spike(extra[:200]))
ax[0,1].set_title("Centered")
ax[1,0].plot(extra[-200:])
ax[1,1].plot(shift_spike(extra[-200:]))
[ax[i,j].xaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{0:g}'.format(x/10))) for i in range(2) for j in range(2)]
plt.show()