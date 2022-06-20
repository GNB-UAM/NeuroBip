import socket
import struct
import select
from time import sleep, time

ip = '127.0.0.1'#'192.168.4.1'

socketSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

i = 0
while True:
    socketSend.sendto(struct.pack("!Bd", i, ((time() / 100) % 1) * 100), (ip, 5000))
    
    msg = select.select([socketSend], [], [], 0.001)
    if len(msg[0]) > 0:
        angles = struct.unpack("!ddddd", socketSend.recv(1024))
        print(angles)
        """
        if abs(angles[0]) >= criticalAngle:
            daq.write([channel], injectionCurrent)
        """

    i = (i + 1) % 3
    sleep(1)