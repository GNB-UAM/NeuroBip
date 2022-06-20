import numpy as np
from scipy.ndimage.interpolation import shift

class Buffer:

    def __init__(self, buffer_size=1000, batch_size=500, drop = 1):
        if batch_size > buffer_size:
            raise ValueError("batch_size must be smaller than buffer_size")
        self.first = 0
        self.last = 0
        self.drop = drop
        self.counter = 0
        self.circularBuffer = np.zeros(buffer_size)
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        

    def add(self, value):
        self.counter += 1
        if self.counter % self.drop == 0:
            self.counter = 0
            self.circularBuffer[self.last] = value
            self.last = (self.last + 1) % self.buffer_size
            if self.last == self.first:
                lastFirst = self.first
                lastLast = (self.last - 1) % self.buffer_size
                self.first = (self.first + self.batch_size) % self.buffer_size

                if lastFirst < lastLast:
                    return center_spike(self.circularBuffer[lastFirst:lastLast + 1])
                else:
                    return center_spike(np.concatenate([self.circularBuffer[lastFirst:],self.circularBuffer[:lastLast + 1]]))
        return None

def center_spike(window):
    return shift(window, (len(window)//2) - np.argmax(window), cval=0)