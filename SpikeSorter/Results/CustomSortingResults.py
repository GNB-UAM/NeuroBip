import pandas as pad
from time import time, sleep
import socket
import struct

SIMULATION = True

fileName = "./data/LPPYPDbegPDend.csv"
dataset = pad.read_csv(fileName, delimiter='\t', header=None, decimal=',')
lp = dataset.iloc[:, 0].to_numpy()/1000
py = dataset.iloc[:, 1].to_numpy()/1000
pd = dataset.iloc[:, 2].to_numpy()/1000
pdEnd = dataset.iloc[:, 3].to_numpy()/1000

ip = '127.0.0.1'#'192.168.4.1'

socketComm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(len(lp) - 1):
    if i % (len(lp)//10) == 0:
        print("{} %".format(i/len(lp)*100))

    lpTime = lp[i]
    pyTime = py[i]
    pdTime = pd[i]
    pdEndTime = pdEnd[i]

    socketComm.sendto(struct.pack("!Bd", 0, lpTime), (ip, 5000))
    if SIMULATION:
        socketComm.sendto(struct.pack("!Bd", 0, lpTime), (ip, 5001))
    sleep(pyTime - lpTime)

    socketComm.sendto(struct.pack("!Bd", 1, pyTime), (ip, 5000))
    if SIMULATION:
        socketComm.sendto(struct.pack("!Bd", 1, pdTime), (ip, 5001))
    sleep(pdTime - pyTime)

    socketComm.sendto(struct.pack("!Bd", 2, pdTime), (ip, 5000))
    if SIMULATION:
        socketComm.sendto(struct.pack("!Bd", 2, pdEndTime), (ip, 5001))
    sleep(lp[i + 1] - pdTime)

print("""===========================================================




                    End of Experiment




===========================================================""")