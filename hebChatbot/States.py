from enum import Enum

class States(Enum):
    EntityExtraction = 1
    IntentRecognition = 2
    ExecutingAction = 3
    ActionDone = 4

    @staticmethod
    def is_edge_state(state):
        return state == States.EntityExtraction or state == States.ActionDone
