import pandas as pd
from Invariant import Invariant
import matplotlib.pyplot as plt
import seaborn as sns

fileName = "./data/sorted_20220611-181030.csv"
dataset = pd.read_csv(fileName, delimiter=',', header=None)
labels = dataset.iloc[:, 0].to_numpy()
times = dataset.iloc[:, 1].to_numpy()

mapInvariant = {'LP': 0, 'PY': 1, 'PD': 2}
mapPeriods1 = {'LP': 1, 'PY': 2, 'PD': 0}
mapPeriods2 = {'LP': 2, 'PY': 0, 'PD': 1}

invariantsClassif = []
periods1Classif = []
periods2Classif = []

for i in range(len(labels)):
    invariantsClassif.append(mapInvariant[labels[i]])
    periods1Classif.append(mapPeriods1[labels[i]])
    periods2Classif.append(mapPeriods2[labels[i]])

invariant = Invariant()
period1 = Invariant()
period2 = Invariant()

invariants = {
    'period': [],
    'inv1': [],
    'inv2': []
}
periods1 = {
    'period': [],
    'inv1': [],
    'inv2': []
}

periods2 = {
    'period': [],
    'inv1': [],
    'inv2': []
}

for i in range(len(labels)):
    period, inv1, inv2 = invariant.calculate(invariantsClassif[i], times[i])
    if period is not None:
        invariants['period'].append(period)
        invariants['inv1'].append(inv1)
        invariants['inv2'].append(inv2)
    period, inv1, inv2 = period1.calculate(periods1Classif[i], times[i])
    if period is not None:
        periods1['period'].append(period)
        periods1['inv1'].append(inv1)
        periods1['inv2'].append(inv2)
    period, inv1, inv2 = period2.calculate(periods2Classif[i], times[i])
    if period is not None:
        periods2['period'].append(period)
        periods2['inv1'].append(inv1)
        periods2['inv2'].append(inv2)

data_dict = {"Period": invariants['period'],
             "LP-PD": invariants['inv1'],
             "PY-PD": invariants['inv2']}

data = pd.DataFrame(data_dict)
sns.pairplot(data)
plt.show()