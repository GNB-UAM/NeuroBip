# %%
# Importing the libraries
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Utils.Buffer import Buffer
from Utils.Normalizer import Normalizer
from Utils.BPFilter import BPFilter
from OldClassifier import OldClassifier
from Utils.IntersectionOverUnion import IntersectionOverUnion

#%matplotlib qt

# %%
# Importing the dataset
filename = os.path.join(parentdir, "datasets/16h_25m_26s.txt")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

extra = dataset.iloc[:, 3].to_numpy()
pd = dataset.iloc[:, 2].to_numpy()
# %%
# Initialize global params
sampleRate = 10000
lowNoise = 50
highNoise = 440

windowsWidth = int(2*20*10)

circularBufferExtra = Buffer(windowsWidth, windowsWidth)
normalizerExtra = Normalizer()

circularBufferPD = Buffer(windowsWidth, windowsWidth)
normalizerPD = Normalizer()

bpFilter = BPFilter(lowNoise, highNoise, sampleRate, order = 5)
oldClassifier = OldClassifier(thresholdLP = 4, LPresistance = 60*10, thresholdPD = 1)

# Train normalizers
filteredDataExtra = bpFilter.filter(extra[:sampleRate*5 if sampleRate*5 < len(extra) else len(extra)])

for data in filteredDataExtra:
    normalizerExtra.calibrate(data)

filteredDataPD = pd[:sampleRate*5 if sampleRate*5 < len(pd) else len(pd)]

for data in filteredDataPD:
    normalizerPD.calibrate(data)

plt.plot(normalizerExtra.normalize(bpFilter.filter(extra[:5*sampleRate])))
plt.plot(normalizerPD.normalize(pd[:5*sampleRate]))
plt.show()

# %%
# Feature extraction
i = 0
classif = []
timesClassif = {'LP': [], 'PY': [],'PD': []}
oldClassif = None

for index, data in enumerate(extra[:]):
    windowsExtra = circularBufferExtra.add(data)
    windowsPD = circularBufferPD.add(pd[index])

    if windowsExtra is not None:
        dataPD = normalizerPD.normalize(windowsPD)
        for indexWindows, dataProcessed in enumerate(normalizerExtra.normalize(bpFilter.filter(windowsExtra))):
            classification = oldClassifier.classify(dataProcessed, dataPD[indexWindows])
            if oldClassif is None:
                oldClassif = classification
            if oldClassif is not classification:
                if len(timesClassif[oldClassif]) > 0:
                    timesClassif[oldClassif][-1].append(index)
                timesClassif[classification].append([index])
                oldClassif = classification
            if classification == 'LP':
                classif.append(2)
            elif classification == 'PY':
                classif.append(1)
            elif classification == 'PD':
                classif.append(0)

plt.plot(extra[:20*sampleRate], label="Original")
plt.plot(classif[:20*sampleRate], label="Classified")
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')
plt.show()

# %%

IOU = IntersectionOverUnion(3)
IOU.calculateFromData(timesClassif['LP'], timesClassif['LP'], 0)
print(IOU.getAccuracies())