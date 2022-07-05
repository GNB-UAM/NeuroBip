from OldClassifier.OldClassifierWrapper import OldClassifierWrapper
from PyComedi.PyComedi import DataAcquisitor
import signal
import time
import matplotlib.pyplot as plt
import sys
import numpy as np
import socket
import struct
import math
import select

def signal_handler(sig, frame):
	global stop
	stop = True
	daq.stopAll()

signal.signal(signal.SIGINT, signal_handler)
socketComm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sampleRate = 10000
ip = '127.0.0.1'#'192.168.4.1'
criticalAngle = 30*math.pi/180 # 60 degrees
injectionCurrent = -0.5/10
stop = False

daq = DataAcquisitor()
oldClassifier = OldClassifierWrapper(thresholdLP = 5, LPresistance = 40*10, thresholdPD = 2, sampleRate = sampleRate, maxCalibrateNormalization=1)

daq.openDevice()
daq.getSession()

previousTime = time.time()
colorNeuron = {'LP' : 0, 'PY' : 1, 'PD' : 2}
mapClassificationClassic = {'LP': 0, 'PY': 1, 'PD': 2}

while not stop:
	detectionTime = ((time.time() / 10000) % 1) * 10000
	pd, extra = daq.read([1, 2])
	classification = oldClassifier.predict(extra, pd)
	if classification is not None:
		socketComm.sendto(struct.pack("!Bd", mapClassificationClassic[classification], detectionTime), (ip, 5000))
		print(classification)

	msg = select.select([socketComm], [], [], 0.001)
	if len(msg[0]) > 0:
		angles = struct.unpack("!ddddd", socketComm.recv(1024))
		#daq.write([0], [injectionCurrent]*abs(angles[0]))
	time.sleep(max(0, 1./sampleRate - (time.time() - detectionTime)))
	
