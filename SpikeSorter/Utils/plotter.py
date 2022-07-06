import pandas as pd 
import matplotlib.pyplot as plt 
import sys
import numpy as np

TIME = 0
EXTRA = 1
INTRA = 2
CLASS = 3


path = sys.argv[1]
#sorter = sys.argv[2]

df = pd.read_csv(path, header = None, delimiter=' ')
data = df.values
#df_sorter = pd.read_csv(sorter, header = None, delimiter=',').values
#df = np.loadtxt(path,delimiter=' ')
#time = np.loadtxt(path,delimiter=' ', usecols=0)
#df_sorter = np.loadtxt(sorter,delimiter=',', usecols=1)

#time = np.arange(0, df["extra"].values.size) * 0.1
print(data[:,TIME], data[:,EXTRA])
#print(df_sorter.groupby()[0])
#print(df_sorter)
plt.plot(data[:,TIME], data[:,EXTRA])
plt.plot(data[:,TIME], data[:,INTRA])
plt.plot(data[:,TIME], data[:,CLASS])
#plt.plot( df["t"].values, df["extra"].values)
#df["extra"].plot()

#plt.plot(df[0].astype(np.float64),df[1].astype(np.float64))
#plt.plot(df_sorter, np.zeros(df_sorter.shape), '|')
plt.show()