import os
import Action

class Entity:
    yes_no_str_buttons = "[כן|לא]"

    def __init__(self, rootDir, entityFileName, spellingFileName, conversationFileName):
        self.entityFileName = entityFileName
        self.spellingFileName = spellingFileName
        self.spelling = []
        self.actions = []
        self.entityNameHeb = ""
        self.InitSpellingBank(rootDir)
        actionsNames = os.listdir(rootDir + '/' + entityFileName)
        for action in actionsNames:
            if("." not in action):
                self.actions.append(Action.Action(rootDir, entityFileName, action, spellingFileName, conversationFileName, self.entityNameHeb))

    def InitSpellingBank(self, rootDir):
        file = open(rootDir + '/' + self.entityFileName + '/' + self.spellingFileName, encoding='utf-8')
        self.spelling = [line.rstrip('\n') for line in file]
        if len(self.spelling) > 0:
            self.entityNameHeb = self.spelling[0]
        file.close()

    def AskUserForAction(self):
        answer_actions = self.strAllActions()
        actions = ""
        if answer_actions[0] == 1:
            bold_action = "<b>" + answer_actions[1] + "</b>"
            actions += "אני רק מוודא, התכוונת ל" + bold_action + "?\n" + self.yes_no_str_buttons
        else:
            actions += "אני רק מוודא, התכוונת ל\n"
            actions += '[' + self.strAllActions() + ']'

        return actions

    def strAllActions(self):
        actions = ""

        if len(self.actions) == 1:
            action = self.actions[0]
            return [1, action.actionNameHeb + ' ' + action.entityNameHeb]
        else:
            for action in self.actions:
                actions += action.actionNameHeb + ' ' + action.entityNameHeb + '|'
            actions = actions[:len(actions) - 1]

        return [len(self.actions), actions]