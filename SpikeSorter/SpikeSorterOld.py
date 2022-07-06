import pandas as pd
import numpy as np
from math import inf, pi
import matplotlib.pyplot as plt
import os
from ThreshClassifier.ThreshClassifierWrapper import ThreshClassifierWrapper
from time import sleep, time, strftime
import socket
import struct
import select
import signal
from PyComedi.PyComedi import DataAcquisitor

LIMIT_ANGLE = pi/4

ONLINE = False
SIMULATION = False
SAVE = True
TIME = 30 # Offline time in minutes

sampleRate = 10000
#    local/simulation   robot
ip = '127.0.0.1'#'192.168.4.1'

if not ONLINE:
    # Importing the dataset
    filename = os.path.join(os.path.dirname(__file__), "datasets/02-Mar-2022/15h42m45s-02-Mar-2022.dat")
    dataset = pd.read_csv(filename, delimiter=' ', header=2)


    extra = dataset.iloc[:, 2].to_numpy()
    pd = dataset.iloc[:, 3].to_numpy()

    #extra = extra[::10]
    #pd = pd[::10]

    '''
    meanPd = np.mean(pd[:5*sampleRate])
    stdPd = np.std(pd[:5*sampleRate])
    normPd = (np.array(pd) - meanPd) / stdPd 

    meanExtra = np.mean(extra[:5*sampleRate])
    stdExtra = np.std(extra[:5*sampleRate])
    normExtra = (np.array(extra) - meanExtra) / stdExtra 

    plt.plot(normExtra[:5*sampleRate], label = 'extra')
    #plt.plot(pd[:5*sampleRate], label = 'pd')
    plt.plot(normPd[:5*sampleRate], label = 'pd')



    plt.legend()
    plt.show()
    '''

else:
    
    def signal_handler(sig, frame):
        daq.stopAll()

    signal.signal(signal.SIGINT, signal_handler)
    daq = DataAcquisitor()
    daq.openDevice()
    daq.getSession()

if SAVE:
    experimentTime = []
    detectedNeurons = []
    detectionTimes = []
    robotAngles = []
    saveExtra = []
    savePd = []
    saveClassification = []



criticalAngle = 1 #RAD 60 degrees 

socketComm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Threshold normalized 4-8
threshClassifier = ThreshClassifierWrapper(thresholdLP = 5.5, thresholdPDLow = 0, thresholdPD = 1, sampleRate = sampleRate)

currenClassif = 'LP_start'
mapClassificationClassic = {'LP_start': 0, 'LP_spike': 1, 'PD_start': 2, 'PD_spike': 3, 'undef': 4}
mapClassificationClassicWorstInvariant1 = {'LP_start': 2, 'LP_spike': 0, 'PD_start': 1}
mapClassificationClassicWorstInvariant2 = {'LP_start': 1, 'LP_spike': 2, 'PD_start': 0}

def classifyAndSend(extra, pd, currentTime, oldAngles):
    global currenClassif, detectedNeurons, detectionTimes
    classification = threshClassifier.predict(extra, pd)
    #detectionTime = ((currentTime / 10000) % 1) * 10000
    detectionTime = currentTime - initialTime
    if classification is not None:
        if currenClassif != classification:
            #print(classification)
            currenClassif = classification

            if SAVE:
                detectedNeurons.append(classification)
                detectionTimes.append(detectionTime)
        
            socketComm.sendto(struct.pack("!Bd", mapClassificationClassic[classification], detectionTime), (ip, 5000))
            if SIMULATION:
                socketComm.sendto(struct.pack("!Bd", mapClassificationClassicWorstInvariant1[classification], detectionTime), (ip, 5001))
                socketComm.sendto(struct.pack("!Bd", mapClassificationClassicWorstInvariant2[classification], detectionTime), (ip, 5002))

    msg = select.select([socketComm], [], [], 0.001)
    if len(msg[0]) > 0:
        angles = list(struct.unpack("!ddddd", socketComm.recv(1024)))
        angles.append(detectionTime)
        return angles
    return oldAngles


injectionCurrent = -1/10
initialTime = time()
nextIntervalTime = initialTime
angles = np.zeros((6,1))
print("Starting")

if not ONLINE:
    for i in range(len(extra)):
        currentTime = time()
        nextIntervalTime = nextIntervalTime + (1.0 / sampleRate)

        #if i % (len(extra)//10) == 0:
        #    print("{} %".format(i/len(extra)*100))

        angles = classifyAndSend(extra[i], pd[i], currentTime, angles)
        

        if angles is not None:
            if abs(angles[0]) >= LIMIT_ANGLE:
                if SAVE:
                    print(i)
                    print("Saving experiment %s: duration %.2fs"%(strftime("%Y%m%d-%H%M%S"), currentTime-initialTime))
                    with open("Results/data/{}_sorted.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
                        for j in range(len(detectedNeurons)):
                            f.write("{},{}\n".format(detectedNeurons[j], detectionTimes[j]))
                    with open("Results/data/{}_angles.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
                        for j in range(len(robotAngles)):
                            f.write("%f %f %f %d"%(experimentTime[j], saveExtra[j], savePd[j], saveClassification[j]))
                            #f.write("{},".format(robotAngles[j]))
                            for angle in robotAngles[j]:
                                f.write(" %f"%(angle))
                            f.write("\n")

                # Clean arrays
                experimentTime = []
                detectedNeurons = []
                detectionTimes = []
                robotAngles = []
                saveExtra = []
                savePd = []
                saveClassification = []
                angles = np.zeros((6,1))
                    


                print("New robot in 5 seconds...")
                sleep(5) # Wait 5s until next robot
                initialTime = time()
            

        experimentTime.append(currentTime - initialTime)
        robotAngles.append(angles)
        saveExtra.append(extra[i])
        savePd.append(pd[i])
        saveClassification.append(mapClassificationClassic[currenClassif])


        sleep(max(0, nextIntervalTime - time()))
else:
    # TODO: change to for with time limit
    while True:
        currentTime = time()
        data = daq.read([2, 1])

        #print("%f %f\n"%(data[0], data[1]))

        angles = classifyAndSend(data[0], data[1], currentTime)
        


        if angles is not None and SAVE:
            """if abs(angles[0]) >= criticalAngle:
                daq.write([0], injectionCurrent)
            else:
                daq.write([0], [0])"""

            if abs(angles[0]) >= LIMIT_ANGLE:
                if SAVE:
                    with open("Results/data/sorted_{}.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
                        for j in range(len(detectedNeurons)):
                            f.write("{},{}\n".format(detectedNeurons[j], detectionTimes[j]))
                    with open("Results/data/angles_{}.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
                        for j in range(len(robotAngles)):
                            f.write("%f %f %f %d"%(experimentTime[j], saveExtra[j], savePd[j], saveClassification[j]))
                            f.write("{},".format(robotAngles[j]))
                            f.write("\n")

                    # Clean arrays
                    experimentTime = []
                    detectedNeurons = []
                    detectionTimes = []
                    robotAngles = []
                    saveExtra = []
                    savePd = []
                    saveClassification = []
                    initialTime = time()


                sleep(5) # Wait 5s until next robot
                
            else:
                experimentTime.append(currentTime - initialTime)
                robotAngles.append(angles)
                saveExtra.append(data[0])
                savePd.append(data[1])
                saveClassification.append(mapClassificationClassic[currenClassif])




        sleep(max(0, 1/sampleRate - (time() - currentTime)))


print("""===========================================================




                    End of Experiment




===========================================================""")
# WARNING NEVER SAVING --> change while True
if SAVE:
    with open("Results/data/sorted_{}.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
        for i in range(len(detectedNeurons)):
            f.write("{},{}\n".format(detectedNeurons[i], detectionTimes[i]))
    with open("Results/data/angles_{}.csv".format(strftime("%Y%m%d-%H%M%S")), "w") as f:
        for i in range(len(robotAngles)):
            f.write("{},".format(robotAngles[i]))
