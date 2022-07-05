import socket
import struct
import numpy as np
from time import sleep
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = '192.168.4.1'
localhost = '127.0.0.1'

times = np.load('times.npy')
sampleRate = 1/10000
lastDeteceted = 0

for time in times:
    if time != lastDeteceted:
        lastDeteceted = time
        socket.sendto(struct.pack("!B", lastDeteceted), (localhost, 5000))

    sleep(sampleRate)