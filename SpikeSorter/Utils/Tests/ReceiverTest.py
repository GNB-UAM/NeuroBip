import socket
import struct
import time
import select

LOCAL_HOST = "127.0.0.1"
IP_SERVER = LOCAL_HOST
PORTRCV = 5000
TIME_OUT = 0.1

sockRCV = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sockRCV.bind((IP_SERVER, PORTRCV))
sockRCV.setblocking(0)

while True:
    lect,escr,err=select.select([sockRCV],[],[], TIME_OUT)
    if len(lect)>0:
        data, addr = sockRCV.recvfrom(2048)
        LP, PY, PD = struct.unpack('!fff', data)
        print("LP: %f, PY: %f, PD: %f" % (LP, PY, PD))
    time.sleep(0.5)