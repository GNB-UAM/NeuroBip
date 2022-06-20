import serial

from Utils.Communication.CommunicationInterface import CommunicationInterface

class CommunicationSerial (CommunicationInterface):

    def __init__(self, port: int, baudrate: int = 19200):
        self.serial = serial.Serial(port, baudrate)

    def close(self) -> bool:
        return self.serial.close()

    def read(self) -> str:
        return self.serial.readline()

    def write(self, LP: float, PY: float, PD: float, LPend: float) -> None:
        self.serial.write(self.encode(LP, PY, PD, LPend))
        self.serial.flush()

    def encode(self, LP: float, PY: float, PD: float, LPend: float) -> str:
        return str((PD - LP) / 30) + "\t" + str((LPend - LP) * 1000) + "\n"