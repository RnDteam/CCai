import os
import Entity as Entity
import States as States
import Logger as Logger
from User import User
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
            return HandleActionFound(user_message, user_message.user.CURRENT_ENTITY.actions[0])

    for word in user_message.message.split(" "):
        for action in user_message.user.CURRENT_ENTITY.actions:
            if word in action.spelling:
                return HandleActionFound(user_message, action)

    return MistakenOrDeniedInFindingAction(user_message)

def MistakenOrDeniedInFindingAction(user_message):
    if IsDenied(user_message.message) or IsMistaken(user_message.message):
        user_message.user.CURRENT_STATE = States.States.EntityExtraction
        return True

    return False

def HandleActionFound(user_message, action):
    Logger.Log.DebugPrint("Found Action")
    user_message.user.CURRENT_ACTION = action
    user_message.user.CURRENT_STATE = States.States.ExecutingAction

    return True

def Start(user_message):
    global CURRENT_STATE
    CURRENT_STATE = States.States.EntityExtraction

    str_to_print = ""
    user = user_message.user
    message = user_message.message

    ''' switch case in python is quite weird. thus using if statements '''
    if user.CURRENT_STATE == States.States.EntityExtraction:
        Logger.Log.DebugPrint("States.EntityExtraction")
        user.is_clear = ExtractEntity(user_message)

        if user.is_clear == False:
            if user.is_mistaken == False:
                str_to_print = "בוא ספר לי מה אתה זומם?\n"
            else:
                str_to_print = "הבנתי שטעית. אז במה תרצה שאטפל?\n"
                user.is_mistaken = False

    if user.CURRENT_STATE == States.States.IntentRecognition:
        Logger.Log.DebugPrint("States.IntentRecognition")
        user.is_clear = FindAction(user_message)

        if user.is_mistaken:
            str_to_print += "הבנתי שטעית.\n"
            user.is_mistaken = False

        ''' This question might be a button later '''
        if not user.is_clear and user.CURRENT_STATE == States.States.IntentRecognition:
            str_to_print += user.CURRENT_ENTITY.AskUserForAction()
            return str_to_print
        elif user.CURRENT_STATE == States.States.IntentRecognition:
            return "אז מה רצונך, אם כך?"
        elif user.CURRENT_STATE != States.States.ExecutingAction:
            return Start(user_message)

    if user.CURRENT_STATE == States.States.ExecutingAction:
        Logger.Log.DebugPrint("Starting to " + user.CURRENT_ACTION.actionName + " " + user.CURRENT_ENTITY.entityFileName)

        answer = user.CURRENT_ACTION.StartConversation(user, message)
        if user.CURRENT_STATE == States.States.IntentRecognition:
            # Reset user message so you won't go another step backward
            user_message.message = ""
            return Start(user_message)
        elif answer != None:
            user.is_mistaken = False
            str_to_print += answer
    if user.CURRENT_STATE == States.States.ActionDone:
        if user.is_asked_yes_no_question:
            if IsApproved(message):
                user.resetUser()
                return "מה בפיך הפעם?"
            elif IsDenied(message):
                str_to_print += "טוב אני סיימתי פה סלאמאת"
                return str_to_print
            else:
                user.is_clear = False
                message = ""

        if user.is_clear == False:
            str_to_print += "\nלא ממש הבנתי. אתה צריך משהו נוסף?"
        else:
            str_to_print += "\nאין בעיה דאגתי לך. יש עוד משהו שאוכל לעזור בו?"

        user.is_asked_yes_no_question = True

    # if (IsMistaken(message) and user.CURRENT_STATE != States.States.EntityExtraction)\
    #         or (IsDenied(message) and user.CURRENT_STATE == States.States.IntentRecognition):
    #     user.CURRENT_STATE = States.States(user.CURRENT_STATE.value - 1)
    #     user.is_mistaken = True

    return str_to_print

if __name__ == '__main__':
    InitEntities()
    Start()