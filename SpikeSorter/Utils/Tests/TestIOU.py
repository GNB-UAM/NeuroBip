import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from IntersectionOverUnion import IntersectionOverUnion

IOU = IntersectionOverUnion(1)
IOU.calculateFromData([[0, 1], [3, 4], [4, 6]], [[0, 1], [3, 4], [4.5, 10]], 0)
print(IOU.intersections, IOU.unions)
print("New: {} %".format(IOU.getAccuracies()*100))