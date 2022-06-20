import pandas as pd
import matplotlib.pyplot as plt
import os
from OldClassifier.OldClassifierWrapper import OldClassifierWrapper
from time import sleep, time, strftime
import socket
import struct
import select

ONLINE = False
SIMULATION = True
SAVE = False
TIME = 30 # Offline time in minutes

if not ONLINE:
    # Importing the dataset
    filename = os.path.join(os.path.dirname(__file__), "datasets/02-Mar-2022/15h42m45s-02-Mar-2022.dat")
    dataset = pd.read_csv(filename, delimiter=' ', header=2)

    sampleRate = 10000

    extra = dataset.iloc[:, 2].to_numpy()
    extra = extra[:TIME*60*sampleRate]
    pd = dataset.iloc[:, 3].to_numpy()

    plt.plot(extra[:5*sampleRate], label = 'extra')
    plt.plot(pd[:5*sampleRate], label = 'pd')
    plt.legend()
    plt.show()

else:
    pass

if SAVE:
    detectedNeurons = []
    detectionTimes = []

ip = '127.0.0.1'#'192.168.4.1'

socketComm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

oldClassifier = OldClassifierWrapper(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2, sampleRate = sampleRate)

currenClassif = 'LP'
mapClassificationClassic = {'LP': 0, 'PY': 1, 'PD': 2}
mapClassificationClassicWorstInvariant1 = {'LP': 2, 'PY': 0, 'PD': 1}
mapClassificationClassicWorstInvariant2 = {'LP': 1, 'PY': 2, 'PD': 0}

def classifyAndSend(currentTime):
    global currenClassif, detectedNeurons, detectionTimes
    classification = oldClassifier.predict(extra[i], pd[i])
    if classification is not None:
        if currenClassif != classification:
            #print(classification)
            currenClassif = classification
            detectionTime = ((currentTime / 10000) % 1) * 10000

            if SAVE:
                detectedNeurons.append(classification)
                detectionTimes.append(detectionTime)
        
            socketComm.sendto(struct.pack("!Bd", mapClassificationClassic[classification], detectionTime), (ip, 5000))
            if SIMULATION:
                socketComm.sendto(struct.pack("!Bd", mapClassificationClassicWorstInvariant1[classification], detectionTime), (ip, 5001))
                socketComm.sendto(struct.pack("!Bd", mapClassificationClassicWorstInvariant2[classification], detectionTime), (ip, 5002))

    msg = select.select([socketComm], [], [], 0.001)
    if len(msg[0]) > 0:
        angles = struct.unpack("!ddddd", socketComm.recv(1024))
        print(angles[0])
        return angles
    
    return None


if not ONLINE:
    for i in range(len(extra)):
        currentTime = time()
        if i % (len(extra)//10) == 0:
            print("{} %".format(i/len(extra)*100))
        classifyAndSend(currentTime)
        sleep(max(0, 1/sampleRate - (time() - currentTime)))

print("""===========================================================




                    End of Experiment




===========================================================""")

if SAVE:
   with open("Results/data/sorted_{}.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
        for i in range(len(detectedNeurons)):
            f.write("{},{}\n".format(detectedNeurons[i], detectionTimes[i]))
