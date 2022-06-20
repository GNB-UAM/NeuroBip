from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

path = "./data/"
files = [f for f in listdir(path) if isfile(join(path, f))]

filenames = []
types = []

meanTimes = []
meanDistances = []
stdsTimes = []
stdsDistances = []
numFalls = []

timeThreshold = 10

for filename in files:
    if filename.endswith(".csv"):
        filenames.append(filename)
        dataset = pd.read_csv(path + filename, delimiter=',', header=None)

        times = dataset.iloc[:, 0].to_numpy()
        distances = dataset.iloc[:, 1].to_numpy()
        port = dataset.iloc[:, 2].to_numpy()

        if np.all(port == port[0]):
            if port[0] == 5000:
                types.append("Invariant")
            elif port[0] == 5001 or port[0] == 5002:
                types.append("NO Invariant")
            else:
                types.append("Unknown")
        else:
            types.append("Mixed")

        validTimes = times[np.nonzero(times > timeThreshold)]
        validDistances = distances[np.nonzero(times > timeThreshold)]

        meanTimes.append(np.mean(validTimes))
        meanDistances.append(np.mean(validDistances))
        stdsTimes.append(np.std(validTimes))
        stdsDistances.append(np.std(validDistances))
        numFalls.append(len(validTimes))

data = [meanTimes, stdsTimes, meanDistances, stdsDistances, numFalls]
header = ["Mean Times", "Std Times", "Mean Distances", "Std Distances", "# Falls"]

print(pd.DataFrame(data, header, types))