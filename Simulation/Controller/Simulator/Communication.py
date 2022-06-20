import socket
import struct
import select

class Communication:

    def __init__(self, port = None):
        self.port = port
        if self.port is not None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(('127.0.0.1', port))
            self.socket.setblocking(False)

            self.address = None

    def receive(self):
        if self.port is not None:
            msg = select.select([self.socket], [], [], 0.001)
            if len(msg[0]) > 0:
                data, self.address = self.socket.recvfrom(1024)
                return struct.unpack("!Bd", data)
        return None

    def send(self, gyroAngle, servoAngles):
        if self.port is not None and self.address is not None:
            self.socket.sendto(struct.pack("!d%sd" % len(servoAngles), gyroAngle, *servoAngles), self.address)
    
    def close(self):
        if self.port is not None:
            self.socket.close()