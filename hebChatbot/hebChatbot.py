import os
import Entity as Entity
import States as States
import Logger as Logger
from UserStatus import IsMistaken, IsApproved, IsDenied

ENTITIES = []
CURRENT_STATE = None
CURRENT_ENTITY = None
CURRENT_ACTION = None

operationDir = 'Operations'
spellingFile = "Spelling.txt"
conversationFile = "Conversation.txt"
entityDir = 'Entities'
rootDir = os.path.join(os.path.dirname(__file__), entityDir)


def InitEntities():
    entities = os.listdir(rootDir)
    for entity in entities:
        ENTITIES.append(Entity.Entity(rootDir, entity, spellingFile, conversationFile))

def ExtractEntity(user_message):
    global CURRENT_STATE
    global CURRENT_ENTITY

    for word in user_message.message.split(" "):
        for entity in ENTITIES:
            if word in entity.spelling:
                Logger.Log.DebugPrint("Found Entity-" + word)
                user_message.user.CURRENT_ENTITY = entity
                user_message.user.CURRENT_STATE = States.States.IntentRecognition
                return True

    return False

def FindAction(user_message):
    global CURRENT_STATE
    global CURRENT_ACTION

    ''' if there's one action - then it is Yes No question '''
    if len(user_message.user.CURRENT_ENTITY.actions) == 1:
        if IsApproved(user_message.message):
            Logger.Log.DebugPrint("Found Action")
            user_message.user.CURRENT_ACTION = CURRENT_ENTITY.actions[0]
            user_message.user.CURRENT_STATE = States.States.ExecutingAction
            return True
        elif IsDenied(user_message.message):
            return False
        else:
            return False
    else:
        for word in user_message.message.split(" "):
            for action in user_message.user.CURRENT_ENTITY.actions:
                if word in action.spelling:
                    Logger.Log.DebugPrint("Found Action-" + word)
                    user_message.user.CURRENT_ACTION = action
                    user_message.user.CURRENT_STATE = States.States.ExecutingAction
                    return True

    return False

def Start(user_message):
    global CURRENT_STATE
    CURRENT_STATE = States.States.EntityExtraction

    user = user_message.user
    message = user_message.message

    print("היי, נבראתי על מנת לחסוך לך זמן.")
    user.is_clear = True
    user.is_mistaken = False
    str_to_print = ""

    ''' switch case in python is quite weird. thus using if statements '''
    if user.CURRENT_STATE == States.States.EntityExtraction:
        if user.is_mistaken == False and user.is_clear == True:
            str_to_print = "בוא ספר לי מה אתה זומם?\n"
        elif user.is_mistaken == True:
            str_to_print = "הבנתי שטעית. אז במה תרצה שאטפל?\n"
            user.is_mistaken = False
        elif user.is_clear == False:
            str_to_print = "תאמת לא הבנתי מה רצית, תרשום שוב\n"

        '''user_input = input(str_to_print)'''

        Logger.Log.DebugPrint("States.EntityExtraction")
        user.is_clear = ExtractEntity(user_message)
    elif user.CURRENT_STATE == States.States.IntentRecognition:
        ''' This question might be a button later '''
        if user.is_mistaken == True:
            str_to_print += "הבנתי שטעית.\n"
            user.is_mistaken = False

        if user.is_clear == True:
            str_to_print += user.CURRENT_ENTITY.AskUserForAction() + '?\n'
            # user_input = input(user.CURRENT_ENTITY.AskUserForAction() + '?\n')
        else:
            str_to_print += "לא אשקר שהבנתי, תנסה לנסח אחרת\n"
            # user_input = input("לא אשקר שהבנתי, תנסה לנסח אחרת\n")

            Logger.Log.DebugPrint("States.IntentRecognition")
        user.is_clear = FindAction(user_message)

    elif user.CURRENT_STATE == States.States.ExecutingAction:
        Logger.Log.DebugPrint("Starting to " + user.CURRENT_ACTION.actionName + " " + user.CURRENT_ENTITY.entityFileName)

        return user.CURRENT_ACTION.StartConversation(user, message)

        ''' If goes back by one state'''
        if user.CURRENT_STATE == States.States(user.CURRENT_STATE.value - 1):
            user.is_clear = False
            user.is_mistaken = True

    elif user.CURRENT_STATE == States.States.ActionDone:
        if user.is_clear == False:
            user_input = input("לא ממש הבנתי. אתה צריך משהו נוסף?\n")
        else:
            user_input = input("אין בעיה דאגתי לך. יש עוד משהו שאוכל לעזור בו?\n")

        if IsApproved(message):
            CURRENT_STATE = States.States.EntityExtraction
            user.is_mistaken = False
            user.is_clear = True
        elif IsDenied(message):
            print("טוב אני סיימתי פה סלאמאת")
            return
        else:
            user.is_clear = False

    if (IsMistaken(message) or IsDenied(message)) and user.CURRENT_STATE != States.States.EntityExtraction:
        user.CURRENT_STATE = States.States(user.CURRENT_STATE.value - 1)
        user.is_mistaken = True

    return str_to_print

if __name__ == '__main__':
    InitEntities()
    Start()