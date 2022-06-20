# %%
# Importing the libraries
from time import time
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from KMeans.KMeansWrapper import KMeansWrapper
from FSM.FSMWrapper import FSMWrapper
from OldClassifier.OldClassifierWrapper import OldClassifierWrapper
from Utils.IntersectionOverUnion import IntersectionOverUnion

#%matplotlib qt

# %%
# Importing the dataset
filename = os.path.join(os.path.dirname(__file__), "datasets/02-Mar-2022/15h36m02s-02-Mar-2022.dat")
dataset = pd.read_csv(filename, delimiter=' ', header=2)

sampleRate = 10000

extra = dataset.iloc[:, 2].to_numpy()
extra = extra[:60*sampleRate]
pd = dataset.iloc[:, 3].to_numpy()

plt.plot(extra[:5*sampleRate], label = 'extra')
plt.plot(pd[:5*sampleRate], label = 'pd')
plt.legend()
plt.show()

# %%
# Initialize global params
windowsWidth = int(200)#2.5*20*10)

classifier = KMeansWrapper(model = "KMeans/models/kmeans_encoder_center.pkl", windowsWidth = windowsWidth, sampleRate = sampleRate)
fsm = FSMWrapper(numChecksNormal = 0, numChecksJump = 0)
oldClassifier = OldClassifierWrapper(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2, sampleRate = sampleRate)
IOU = IntersectionOverUnion(num_classes = 3)

# %%
mapClassificationKM = {'LP': ['red', 2], 'PY': ['blue', 0], 'PD': ['green', 1]}
mapClassificationClassic = {'LP': ['blue', 0], 'PY': ['green', 1], 'PD': ['red', 2]}

# %%
# Classify
classif = []
currenClassif = 'LP'
classifTimes = [[], [], []]
maxTime = 0
currentTime = 0
startTime = time.time()

print("Classifying...")

for i in range(len(extra)):
    #time.sleep(max((1/sampleRate) - (time.time() - currentTime), 0))
    currentTime = time.time()
    classification = fsm.predict(classifier.predict(extra[i]))
    maxTime = max(maxTime, time.time() - currentTime)
    if classification is not None:
        if currenClassif != classification:
            if len(classifTimes[mapClassificationKM[currenClassif][1]]) > 0:
                classifTimes[mapClassificationKM[currenClassif][1]][-1].append(i)
            classifTimes[mapClassificationKM[classification][1]].append([i])
        currenClassif = classification
    classif.append(mapClassificationKM[currenClassif][0])

#print("Max time K-Means: {}, lost windows: {} %, exceeded time: {} s".format(maxTime, 100 * classifier.lostWindows / classifier.totalWindows, (time.time() - startTime) - 60))
print("Max time K-Means: {}".format(maxTime))
# %%
# Old Classify
classifOld = []
currenClassif = 'LP'
classifOldTimes = [[], [], []]
maxTime = 0

for i in range(len(extra)):
    currentTime = time.time()
    classification = oldClassifier.predict(extra[i], pd[i])
    maxTime = max(maxTime, time.time() - currentTime)
    if classification is not None:
        if currenClassif != classification:
            if len(classifOldTimes[mapClassificationClassic[currenClassif][1]]) > 0:
                classifOldTimes[mapClassificationClassic[currenClassif][1]][-1].append(i)
            classifOldTimes[mapClassificationClassic[classification][1]].append([i])
        currenClassif = classification
    classifOld.append(mapClassificationClassic[currenClassif][0])

print("Max time Old Classifier: " + str(maxTime))

# %%
# Accuracy
for i in range(3):
    # Remove last element incomplete
    classifTimes[i] = classifTimes[i][:-1]
    classifOldTimes[i] = classifOldTimes[i][:-1]
    IOU.calculateFromData(classifTimes[i], classifOldTimes[i], i)

print("Total Accuracy: " + str(IOU.getTotalAccuracy()*100) + " %")
print("Accuracies: LP {} %, PY {} %, PD {}%".format(IOU.getAccuracies()[0]*100, IOU.getAccuracies()[1]*100, IOU.getAccuracies()[2]*100))
# %%
# Plot results
startPlot = 0
endPlot = 40*sampleRate
plt.figure()
plt.scatter(list(range(startPlot, endPlot)), extra[startPlot:endPlot], c=classif[startPlot:endPlot], s=5, label="KMeans Classifier")
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')

plt.figure()
plt.scatter(list(range(startPlot, endPlot)), extra[startPlot:endPlot], c=classifOld[startPlot:endPlot], s=5, label="Old Classifier")
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.legend(loc='best')
plt.show()