import pandas as pad
import matplotlib.pyplot as plt
import seaborn as sns

fileName = "./data/LPPYPDbegPDend.csv"
dataset = pad.read_csv(fileName, delimiter='\t', header=None, decimal=',')
lp = dataset.iloc[:, 0].to_numpy()
py = dataset.iloc[:, 1].to_numpy()
pd = dataset.iloc[:, 2].to_numpy()
pdEnd = dataset.iloc[:, 3].to_numpy()

periods = lp[1:] - lp[:-1]
inv1 = pd - lp
inv2 = pd - py

worstPeriod1 = pdEnd - lp
worstPeriod2 = pdEnd - pd

data_dict_invariant = {"Period": periods,
             "LP-PD": inv1[:-1],
             "PY-PD": inv2[:-1],}

data_dict_other = {"Period": periods,
             "LP-PD": worstPeriod1[:-1],
             "PD Burst": worstPeriod2[:-1],}

data = pad.DataFrame(data_dict_invariant)
sns.pairplot(data)
plt.show()

data = pad.DataFrame(data_dict_other)
sns.pairplot(data)
plt.show()