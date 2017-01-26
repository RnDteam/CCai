import os
import Action

class Entity:

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

    def AskUserForAction(self):
        ''' TODO check if there are two action -
        but for now the default behaviour is to ask user to what action he meant '''

        actions = "רק לוודא, התכוונת ל\n"
        for action in self.actions:
            actions += action.actionNameHeb + ' ' + action.entityNameHeb + '\nאו\n'

        if len(actions) > 3:
            actions = actions[:len(actions) - 4]

        return actions