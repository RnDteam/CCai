import os
import Entity, States, Logger, UserStatus

ENTITIES = []
CURRENT_STATE = None
CURRENT_ENTITY = None
CURRENT_ACTION = None

operationDir = 'Operations'
spellingFile = "Spelling.txt"
conversationFile = "Conversation.txt"
entityDir = 'Entities'
rootDir = os.path.join(os.path.dirname(__file__), entityDir)

UserStatus.UserMemory()

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
                Logger.Log.DebugPrint("Found Entity-" + word)
                CURRENT_ENTITY = entity
                CURRENT_STATE = States.States.IntentRecognition
                return True

    return False

def FindAction(user_input):
    global CURRENT_STATE
    global CURRENT_ACTION

    ''' if there's one action - then it is Yes No question '''
    if len(CURRENT_ENTITY.actions) == 1:
        if UserStatus.IsApproved(user_input):
            Logger.Log.DebugPrint("Found Action")
            CURRENT_ACTION = CURRENT_ENTITY.actions[0]
            CURRENT_STATE = States.States.ExecutingAction
            return True
        elif UserStatus.IsDenied(user_input):
            return False
        else:
            return False
    else:
        for word in user_input.split(" "):
            for action in CURRENT_ENTITY.actions:
                if word in action.spelling:
                    Logger.Log.DebugPrint("Found Action-" + word)
                    CURRENT_ACTION = action
                    CURRENT_STATE = States.States.ExecutingAction
                    return True

    return False

def Start():
    global CURRENT_STATE
    CURRENT_STATE = States.States.EntityExtraction

    print("היי, נבראתי על מנת לחסוך לך זמן.")
    isClear = True
    isMistaken = False
    strPrint = ""
    user_input = None

    while user_input != "end":
        ''' switch case in python is quite weird. thus using if statements '''
        if CURRENT_STATE == States.States.EntityExtraction:
            if isMistaken == False and isClear == True:
                strPrint = "בוא ספר לי מה אתה זומם?\n"
            elif isMistaken == True:
                strPrint = "הבנתי שטעית. אז במה תרצה שאטפל?\n"
                isMistaken = False
            elif isClear == False:
                strPrint = "תאמת לא הבנתי מה רצית, תרשום שוב\n"

            user_input = input(strPrint)

            Logger.Log.DebugPrint("States.EntityExtraction")
            isClear = ExtractEntity(user_input)
        if CURRENT_STATE == States.States.IntentRecognition:
            ''' This question might be a button later '''
            if isMistaken == True:
                print("הבנתי שטעית.\n")
                isMistaken = False

            if isClear == True:
                user_input = input(CURRENT_ENTITY.AskUserForAction() + '?\n')
            else:
                user_input = input("לא אשקר שהבנתי, תנסה לנסח אחרת\n")

                Logger.Log.DebugPrint("States.IntentRecognition")
            isClear = FindAction(user_input)

        if CURRENT_STATE == States.States.ExecutingAction:
            Logger.Log.DebugPrint("Starting to " + CURRENT_ACTION.actionName + " " + CURRENT_ENTITY.entityFileName)

            CURRENT_STATE = CURRENT_ACTION.StartConversation()

            ''' If goes back by one state'''
            if(CURRENT_STATE == States.States(CURRENT_STATE.value - 1)):
                isClear = False
                isMistaken = True

        if CURRENT_STATE == States.States.ActionDone:
            if isClear == False:
                user_input = input("לא ממש הבנתי. אתה צריך משהו נוסף?\n")
            else:
                user_input = input("אין בעיה דאגתי לך. יש עוד משהו שאוכל לעזור בו?\n")

            if UserStatus.IsApproved(user_input):
                CURRENT_STATE = States.States.EntityExtraction
                isMistaken = False
                isClear = True
            elif UserStatus.IsDenied(user_input):
                print("טוב אני סיימתי פה סלאמאת")
                break
            else:
                isClear = False

        if UserStatus.IsMistaken(user_input) and CURRENT_STATE != States.States.EntityExtraction:
            CURRENT_STATE = States.States(CURRENT_STATE.value - 1)
            isMistaken = True

if __name__ == '__main__':
    InitEntities()
    Start()