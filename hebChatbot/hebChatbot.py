#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Entity as Entity
import States as States
import Logger as Logger
from User import User
from UserStatus import IsMistaken, IsApproved, IsDenied

ENTITIES = []

ResetUserChat = "פניה חדשה"
operationDir = 'Operations'
spellingFile = "Spelling.txt"
conversationFile = "Conversation.txt"
entityDir = 'Entities'
rootDir = os.path.join(os.path.dirname(__file__), entityDir)
str_actions = ""
yes_no_str_buttons = "[כן|לא]"

# TODO change name to init all
def InitEntities():
    global str_actions

    entities = os.listdir(rootDir)
    for entity in entities:
        ENTITIES.append(Entity.Entity(rootDir, entity, spellingFile, conversationFile))

    str_actions = InitActionsHelper()

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

def InitActionsHelper():
    actions = "["
    for entity in ENTITIES:
        actions += entity.strAllActions()[1] + "|"
    actions = actions[:len(actions) - 1]
    actions += ']'
    return actions

def MistakenOrDeniedInFindingAction(user_message):
    if IsDenied(user_message.message) or IsMistaken(user_message.message):
        user_message.user.CURRENT_STATE = States.States.EntityExtraction
        user_message.user.is_mistaken = True
        return True

    return False

def HandleActionFound(user_message, action):
    Logger.Log.DebugPrint("Found Action")
    user_message.user.CURRENT_ACTION = action
    user_message.user.CURRENT_STATE = States.States.ExecutingAction

    return True

def Start(user_message):
    str_to_print = ""
    user = user_message.user
    message = user_message.message

    if message == ResetUserChat:
        user.resetUser()
        message = "בוא נתחיל"

    if user.CURRENT_STATE == States.States.EntityExtraction:
        Logger.Log.DebugPrint("States.EntityExtraction")
        if message == "בוא נתחיל":
            str_to_print += "במה אני יכול לעזור?"
        elif message == "תדריך אותי":
            str_to_print += "אני די חדש בתחום. ולכן, אני יודע לעשות מספר פעלות מצומצמות.\n תראה כמה דוגמאות\n" + str_actions + "\n"
            str_to_print += "במידה ואתה רוצה לעשות פעולה אחרת, אתה מוזמן בכל זאת לנסות.\n"
            str_to_print += " בכל זאת אין לך סבלנות לחכות עד שאני אלמד,\n אתה יכול להתקשר ל012 ולדבר עם החברים שלי."
        else:
            user.is_clear = ExtractEntity(user_message)

            if user.is_clear == False:
                if user.is_mistaken == False:
                    str_to_print = "לא הבנתי אותך... \n אני די חדש בתחום. ולכן, אני יודע לעשות מספר פעלות מצומצמות.\n תראה כמה דוגמאות\n" + str_actions
                else:
                    str_to_print = "אוקיי אז במה תרצה שאטפל?\n"
                    user.is_mistaken = False

    if user.CURRENT_STATE == States.States.IntentRecognition:
        Logger.Log.DebugPrint("States.IntentRecognition")
        user.is_clear = FindAction(user_message)

        if user.is_mistaken and not user.is_clear:
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
        if message == "ביי":
            return "ביי"
        if user.is_asked_yes_no_question:
            if user.is_mistaken:
                str_to_print += "אוקיי אולי לא הבנתי אותך.\n"
            if IsApproved(message):
                user.resetUser()
                return "במה אוכל עוד לעזור?"
            elif IsDenied(message):
                str_to_print += "טוב מקווה שעזרתי. להתראות!"
                return str_to_print
            else:
                user.is_clear = False
                message = ""

        if user.is_clear == False:
            str_to_print += "לא ממש הבנתי. אתה צריך משהו נוסף?" + yes_no_str_buttons
        else:
            str_to_print += "אוקיי, יש עוד משהו שאוכל לעזור בו?" + yes_no_str_buttons

        user.is_asked_yes_no_question = True

    # if (IsMistaken(message) and user.CURRENT_STATE != States.States.EntityExtraction)\
    #         or (IsDenied(message) and user.CURRENT_STATE == States.States.IntentRecognition):
    #     user.CURRENT_STATE = States.States(user.CURRENT_STATE.value - 1)
    #     user.is_mistaken = True

    return str_to_print

if __name__ == '__main__':
    InitEntities()
    Start()