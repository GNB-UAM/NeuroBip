import socket
import select
import struct

port = 5000
ip = '127.0.0.1'#'192.168.4.1'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((ip, port))
socket.setblocking(False)

i=0

while True:
    msg = select.select([socket], [], [], 0.001)
    if len(msg[0]) > 0:
        data, address = socket.recvfrom(1024)
        print(struct.unpack("!Bd", data))
        socket.sendto(struct.pack("!B", i), address)
        i += 1