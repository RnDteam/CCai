from enum import Enum

class States(Enum):
    EntityExtraction = 1
    IntentRecognition = 2
    ExecutingAction = 3
    ActionDone = 4
