import numpy as np

class IntersectionOverUnion:

    def __init__(self, num_classes):
        self.accuracies = np.zeros(num_classes)
        self.intersections = np.zeros(num_classes)
        self.unions = np.zeros(num_classes)

    def getAccuracies(self):
        return self.accuracies

    def getTotalAccuracy(self):
        return sum(self.accuracies) / len(self.accuracies)

    def calculateFromData(self, classTimes, targetClassTimes, targetClass):
        i = j = 0

        n = len(classTimes)
        m = len(targetClassTimes)
    
        while i < n and j < m:
            
            l = max(classTimes[i][0], targetClassTimes[j][0])
            r = min(classTimes[i][1], targetClassTimes[j][1])
            
            if l <= r:
                self.intersections[targetClass] += r - l
    
            if classTimes[i][1] < targetClassTimes[j][1]:
                self.unions[targetClass] += classTimes[i][1] - classTimes[i][0]
                i += 1
            else:
                self.unions[targetClass] += targetClassTimes[j][1] - targetClassTimes[j][0]
                j += 1

        while i < n:
            self.unions[targetClass] += classTimes[i][1] - classTimes[i][0]
            i += 1
            
        while j < m:
            self.unions[targetClass] += targetClassTimes[j][1] - targetClassTimes[j][0]
            j += 1

        self.accuracies[targetClass] = self.intersections[targetClass] / float(self.unions[targetClass] - self.intersections[targetClass])
