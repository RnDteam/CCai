import os
import hebChatbot.Entity as Entity
import hebChatbot.States as States
import hebChatbot.Logger as Logger
import hebChatbot.UserStatus as UserStatus

ENTITIES = []
CURRENT_STATE = None
CURRENT_ENTITY = None
CURRENT_ACTION = None

entityDir = 'Entities'

rootDir = os.path.join(os.path.dirname(__file__), entityDir)
print(rootDir)
operationDir = 'Operations'
spellingFile = "Spelling.txt"
conversationFile = "Conversation.txt"

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

    user_input = input("היי, נבראתי על מנת לחסוך לך זמן.\n בוא ספר לי מה אתה זומם?\n")
    isClear = True
    isMistaken = False

    while user_input != "end":
        ''' switch case in python is quite weird. thus using if statements '''
        if CURRENT_STATE == States.States.EntityExtraction:
            Logger.Log.DebugPrint("States.EntityExtraction")

            if isMistaken == True:
                user_input = input("הבנתי שטעית. אז במה תרצה שאטפל?\n")
                isMistaken = False
            elif isClear == False:
                user_input = input("תאמת לא הבנתי מה רצית, תרשום שוב\n")

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
            ''' TODO: ask if user need something else '''
            print("טוב אני סיימתי פה סלאמאת")
            break

        ''' TODO: instead of טעיתי create a file with all synonyms for it '''
        if UserStatus.IsMistaken(user_input) and CURRENT_STATE != States.States.EntityExtraction:
            CURRENT_STATE = States.States(CURRENT_STATE.value - 1)
            isMistaken = True

if __name__ == '__main__':
    InitEntities()
    Start()