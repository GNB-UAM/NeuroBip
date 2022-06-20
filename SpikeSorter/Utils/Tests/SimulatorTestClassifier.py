import socket
import struct
import time

LOCAL_HOST = "127.0.0.1"
IPDST = LOCAL_HOST
PORTDST = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
LP = 1.34534321312312312
PY = 2.3
PD = 3.6

while True:
    msg = struct.pack('!fff', LP, PY, PD)
    sock.sendto(msg, (IPDST, PORTDST))
    time.sleep(1)