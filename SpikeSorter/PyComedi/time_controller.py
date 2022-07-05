import signal
import socket
from PyComedi import DataAcquisitor
import struct
import time

def signal_handler(sig, frame):
    daq.stopAll()

signal.signal(signal.SIGINT, signal_handler)
daq = DataAcquisitor()
daq.openDevice()
daq.getSession()

ip = '192.168.4.1'
socketComm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Starting")
while True:
    daq.write([0], [1])
    socketComm.sendto(struct.pack("!Bd", 0, ((time.time() / 10000) % 1) * 10000), (ip, 5000))
    time.sleep(0.3)
    daq.write([0], [0])
    socketComm.sendto(struct.pack("!Bd", 1, ((time.time() / 10000) % 1) * 10000), (ip, 5000))
    time.sleep(0.3)
    socketComm.sendto(struct.pack("!Bd", 2, ((time.time() / 10000) % 1) * 10000), (ip, 5000))
    time.sleep(0.3)