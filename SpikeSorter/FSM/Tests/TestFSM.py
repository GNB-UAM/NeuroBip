import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from FSM import CarcinusFSM

carcinusFSM = CarcinusFSM(1, 2)
carcinusFSM.storeDFA(path = currentdir)

"""
carcinusFSM.changeState(mapLabel(label))
carcinusFSM.getState()
"""