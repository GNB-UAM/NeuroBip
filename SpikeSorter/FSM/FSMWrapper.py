from FSM.FSM import CarcinusFSM

class FSMWrapper:

    def __init__(self, numChecksNormal = 1, numChecksJump = 2):
        self.numChecksNormal = numChecksNormal
        self.numChecksJump = numChecksJump
        self.carcinusFSM = CarcinusFSM(self.numChecksNormal, self.numChecksJump)

    def predict(self, label):
        return self.carcinusFSM.changeState(label) if label is not None else None