import os
import Entity
import States

CURRENT_STATE = None
CURRENT_ENTITY = None
CURRENT_ACTION = None

ENTITIES = []
rootDir = 'C:/Users/User/PycharmProjects/hebChatbot/Entities'
operationDir = 'Operations'
spellingFile = "Spelling.txt"
conversationFile = "Conversation.txt"

def DebugPrint(text):
    print("<- " + text + " ->\n")

def InitEntities():
    entities = os.listdir(rootDir)
    for entity in entities:
        ENTITIES.append(Entity.Entity(rootDir, entity, spellingFile, conversationFile))

def ExtractEntity(user_input):
    global CURRENT_STATE
    global CURRENT_ENTITY

    for word in user_input.split(" "):
        for entity in ENTITIES:
            if word in entity.spelling:
                DebugPrint("Found Entity-" + word)
                CURRENT_ENTITY = entity
                CURRENT_STATE = States.States.IntentRecognition
                return True

    return False

def FindIntent(user_input):
    global CURRENT_STATE
    global CURRENT_ACTION

    for word in user_input.split(" "):
        for action in CURRENT_ENTITY.actions:
            if word in action.spelling:
                DebugPrint("Found Action-" + word)
                CURRENT_ACTION = action
                CURRENT_STATE = States.States.ExecutingAction
                return True

    return False

def Start():
    global CURRENT_STATE
    CURRENT_STATE = States.States.EntityExtraction

    user_input = None
    isClear = True

    while user_input != "end":
        ''' switch case in python is quite weird. thus using if statements '''
        if CURRENT_STATE == States.States.EntityExtraction:
            DebugPrint("States.EntityExtraction")

            user_input = input("היי, נבראתי על מנת לחסוך לך זמן.\n בוא ספר לי מה אתה זומם?\n")

            isClear = ExtractEntity(user_input)

        if CURRENT_STATE == States.States.IntentRecognition:
            ''' This question might be button later '''
            user_input = input(CURRENT_ENTITY.AskUserForAction() + '?\n')

            DebugPrint("States.IntentRecognition")
            isClear = FindIntent(user_input)
        if CURRENT_STATE == States.States.ExecutingAction:
            DebugPrint("Starting to " + CURRENT_ACTION.actionName + " " + CURRENT_ENTITY.entityFileName)

            CURRENT_STATE = CURRENT_ACTION.StartConversation()
        if CURRENT_STATE == States.States.ActionDone:
            print("טוב אני סיימתי פה סלאמאת")
            break
if __name__ == '__main__':
    InitEntities()
    Start()