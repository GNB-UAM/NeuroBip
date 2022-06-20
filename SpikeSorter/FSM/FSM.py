from PySimpleAutomata import DFA, automata_IO
import os

Sequence = ["LP", "PY", "PD"]

# dfa_example = automata_IO.dfa_dot_importer(os.path.join(os.path.dirname(__file__), "automatas/input.dot"))

#new_dfa = DFA.dfa_minimization(dfa_example)
def baseDFA():
    # Add rankdir=LR to dot file to get a left-to-right graph
    alphabet = ["D" + detect.lower() for detect in Sequence]
    baseDFA = {
        "alphabet": {alpha for alpha in alphabet},
        "states": {state for state in Sequence},
        "initial_state": Sequence[0],
        "accepting_states": {Sequence[0]},
        "transitions": {
            (Sequence[i], alphabet[(i + 1) % len(Sequence)]): Sequence[(i + 1) % len(Sequence)] for i in range(len(Sequence))
        }
    }

    return baseDFA

# ND = NotDetected, D = Detected, DNW = DetectedNormalWait
def buildNormalFlow(numChecks, neuron, base):
    nextNeuron = Sequence[(neuron + 1) % len(Sequence)]
    for i in range(1, numChecks + 1):
        base["states"].add("DNW" + nextNeuron + str(i))
        if i == 1:
            base["transitions"][(Sequence[neuron], "D" + nextNeuron.lower())] = "DNW" + nextNeuron + str(i)
        else:
            base["transitions"][("DNW" + nextNeuron + str(i - 1), "D" + nextNeuron.lower())] = "DNW" + nextNeuron + str(i)

        # If it detects another that is not the next one, it gets back to the base previous state
        base["transitions"][("DNW" + nextNeuron + str(i), "ND")] = Sequence[neuron]

        if i == numChecks:
            base["transitions"][("DNW" + nextNeuron + str(i), "D" + nextNeuron.lower())] = nextNeuron
    
    return base

def buildJumpFlow(numChecks, neuron, base):
    for otherNeuron in range(len(Sequence)):
        # Avoid redundancy on self and next neuron
        if otherNeuron == neuron or otherNeuron == (neuron + 1) % len(Sequence):
            continue

        jumpNeuron = Sequence[otherNeuron]
        for i in range(1, numChecks + 1):
            base["states"].add("DJW" + jumpNeuron + str(i))
            if i == 1:
                base["transitions"][(Sequence[neuron], "D" + jumpNeuron.lower())] = "DJW" + jumpNeuron + str(i)
            else:
                base["transitions"][("DJW" + jumpNeuron + str(i - 1), "D" + jumpNeuron.lower())] = "DJW" + jumpNeuron + str(i)

            # If it detects another that is not the next one, it gets back to the base previous state
            base["transitions"][("DJW" + jumpNeuron + str(i), "ND")] = Sequence[neuron]

            if i == numChecks:
                base["transitions"][("DJW" + jumpNeuron + str(i), "D" + jumpNeuron.lower())] = jumpNeuron
    
    return base

def detectionCheck(numChecksNormal, numChecksJump):
    base = baseDFA()
    
    for neuron in range(len(Sequence)):
        base = buildNormalFlow(numChecksNormal, neuron, base)

    for neuron in range(len(Sequence)):
        base = buildJumpFlow(numChecksJump, neuron, base)
    
    return base

class CarcinusFSM:

    def __init__(self, numChecksNormal, numChecksJump):
        self.dfa = detectionCheck(numChecksNormal, numChecksJump)
        self.baseState = Sequence[0]
        self.state = Sequence[0]

    def storeDFA(self, name = 'baseCarcinusDFA', path = ''):
        automata_IO.dfa_to_dot(self.dfa, name, path + '/automatas')

    def getState(self):
        return self.baseState

    def changeState(self, newState):
        if newState not in Sequence:
            return
        
        transition = "D" + newState.lower()

        if (self.state, transition) not in self.dfa["transitions"]:
            if (self.state, "ND") not in self.dfa["transitions"]:
                nextState = self.state
            else:
                nextState = self.dfa["transitions"][(self.state, "ND")]
        else:
            nextState = self.dfa["transitions"][(self.state, transition)]

        self.state = nextState
        if nextState in Sequence:
            if self.baseState != nextState:
                self.baseState = nextState
                return self.baseState
            self.baseState = nextState

        return None

#new_dfa=DFA.dfa_minimization(dfaCarcinus)