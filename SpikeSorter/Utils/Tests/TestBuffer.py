import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Buffer import Buffer

buf = Buffer(4, 2, 2)

for i in range(16):
    ret = buf.add(i)
    if ret is not None:
        print(ret)