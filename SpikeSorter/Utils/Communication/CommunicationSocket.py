import socket
import struct

from Utils.Communication.CommunicationInterface import CommunicationInterface

class CommunicationSocket (CommunicationInterface):

    def __init__(self, port: int, ip: str = "127.0.0.1"):
        self.numSequence = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def close(self) -> bool:
        return self.socket.close()

    def read(self):
        return self.decode(self.socket.recv(1024))

    def write(self, LP: float, PY: float, PD: float, LPend: float) -> None:
        self.socket.send(self.encode(LP, PY, PD, LPend))
        self.numSequence += 1

    def encode(self, LP: float, PY: float, PD: float, LPend: float):
        return struct.pack("!Hffff", self.numSequence, LP, PY, PD, LPend)

    def decode(self, data: bytes):
        return struct.unpack("!Hfffff", data)