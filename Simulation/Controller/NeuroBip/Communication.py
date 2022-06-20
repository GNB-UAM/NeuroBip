import network
import socket
import struct
import select

class Communication:

    def __init__(self, name = "NeuroBip", psswd = "", port = 5000):
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=name, password=psswd)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('192.168.4.1', port))
        self.socket.setblocking(False)

        self.address = None

    def receive(self):
        msg = select.select([self.socket], [], [], 0.001)
        if len(msg[0]) > 0:
            data, self.address = self.socket.recvfrom(1024)
            return struct.unpack("!Bd", data)
        return None

    def send(self, gyroAngle, servoAngles):
        if self.address is not None:
            self.socket.sendto(struct.pack("!d%sd" % len(servoAngles), gyroAngle, *servoAngles), self.address)
