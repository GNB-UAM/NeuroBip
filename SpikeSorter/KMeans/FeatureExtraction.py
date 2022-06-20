import numpy as np
from sklearn.decomposition import PCA

def featureExtraction(window):
    feature = []
    feature.append(energy(window))#envelopingEnergy(window, 10))
    feature.append(amplitude(window))
    feature.append(meanPonderateFreq(window))
    return feature

def PCA(window):
    return PCA(n_components=3).fit_transform()

def amplitude(window):
    return np.max(window)

def meanPonderateFreq(window):
    fftValues = np.abs(np.fft.fft(window))
    return np.sum(np.multiply(fftValues, np.arange(1, len(fftValues)+1))) / np.sum(fftValues)

def maxFrequency(widnows):
    fftValues = np.abs(np.fft.fft(widnows))
    result = np.argmax(fftValues)
    return result

def energy(window):
    return np.sum(np.square(window))

def envelopingEnergy(window, precission):
    energy = 0
    
    i = 0
    while i < len(window):
        points = len(window)//precission
        piece = window[i:i+points]
        localAmplitude = amplitude(piece)
        energy += localAmplitude*points
        
        i += points

    return energy