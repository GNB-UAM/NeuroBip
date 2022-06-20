from scipy.signal import butter, lfilter

class BPFilter:

    def __init__(self, lowcut, highcut, fs, order=5):
        self.lowcut = lowcut
        self.highcut = highcut
        self.fs = fs
        self.order = order
        self.b, self.a = butter_bandpass(lowcut, highcut, fs, order=order)
        self.z = 1

    def filter(self, data):
        filtered, self.z = lfilter(self.b, self.a, [data], zi = self.z)
        return filtered

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a