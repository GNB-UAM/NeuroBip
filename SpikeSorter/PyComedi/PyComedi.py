import ctypes as ct
import os
import time
import threading

def wrap_function(lib, funcname, argtypes, restype):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

class Daq_session(ct.Structure):
    _fields_ = [("device", ct.c_void_p), 
                ("in_subdev", ct.c_int),
                ("out_subdev", ct.c_int),
                ("range", ct.c_int),
                ("aref", ct.c_int),]

class DataAcquisitor:
    
    def __init__(self):
        self.libc = ct.CDLL(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "comedi_functions.so"))
        self.device = ct.c_void_p()
        self.session_ptr = ct.POINTER(Daq_session)()
        self.stop = False

    def openDevice(self):
        func = wrap_function(self.libc, "daq_open_device", [ct.c_void_p], ct.c_int)
        return func(ct.byref(self.device))

    def closeDevice(self):
        func = wrap_function(self.libc, "daq_close_device", [ct.c_void_p], ct.c_int)
        return func(ct.byref(self.device))
        
    def getSession(self):
        func = wrap_function(self.libc, "daq_create_session", [ct.c_void_p, ct.POINTER(ct.POINTER(Daq_session))], ct.c_int)
        return func(ct.byref(self.device), ct.byref(self.session_ptr))

    def read(self, channels):
        func = wrap_function(self.libc, "daq_read", [ct.POINTER(Daq_session), ct.c_int, ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)], ct.c_int)
        array_channels = (ct.c_int * len(channels))(*channels)
        result = (ct.c_double * len(channels))()
        if func(self.session_ptr, len(channels), array_channels, result) == 0:
            return result

    def write(self, channels, data):
        func = wrap_function(self.libc, "daq_write", [ct.POINTER(Daq_session), ct.c_int, ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)], ct.c_int)
        array_channels = (ct.c_int * len(channels))(*channels)
        array_data = (ct.c_double * len(channels))(*data)
        if func(self.session_ptr, len(channels), array_channels, array_data) == 0:
            return True

    def cleanChannels(self):
        self.write([0,1], [0,0])

    def setFrequency(self, freq):
        self.freq = freq

    def runReading(self):
        self.thread = threading.Thread(target=self.readingThread)
        self.thread.start()

    def readingThread(self):
        self.previousTime = time.time()
        while not self.stop:
            time.sleep(max(0, 1/self.freq - (time.time() - self.previousTime)))
            daq.write([0], daq.read([0]))


    def stopAll(self):
        self.stop = True
        if self.thread is not None:
            self.thread.join()
        daq.cleanChannels()
        daq.closeDevice()
        


import signal

def signal_handler(sig, frame):
    daq.stopAll()

signal.signal(signal.SIGINT, signal_handler)
daq = DataAcquisitor()
daq.openDevice()
daq.getSession()
daq.setFrequency(10000)
daq.runReading()
