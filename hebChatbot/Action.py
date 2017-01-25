import States, Parser, Logger

class Action:
    def __init__(self, rootDir, entityName, actionName, spellingFileName, conversationFileName, entityNameHeb):
        self.rootDir = rootDir
        self.entityName = entityName
        self.actionName = actionName
        self.entityNameHeb = entityNameHeb
        self.spellingFileName = spellingFileName
        self.conversationFileName = conversationFileName

        self.spelling = []
        self.conversation = []
        self.InitSpellingBank()

    def InitSpellingBank(self):
        file = open(self.rootDir + '/' + self.entityName + '/' + self.actionName + '/' + self.spellingFileName, encoding='utf-8')
        self.spelling = [line.rstrip('\n') for line in file]
        self.actionNameHeb = self.spelling[0]

    def StartConversation(self):
        user_input = None
        convMemory = {}

        file = open(self.rootDir + '/' + self.entityName + '/' + self.actionName + '/' + self.conversationFileName,
                    encoding='utf-8')
        self.conversation = [line.rstrip('\n') for line in file]
        for row_input in self.conversation:
            ''' We would prefer to have a parser class
             which handles the conversation file '''
            if row_input.startswith("out:"):
                ''' A output row might have a variable in it
                but as we create a parser class we would implement that'''
                print(row_input.split("out:")[1])
            elif row_input.startswith("in:"):
                input_validation = row_input.split("in:")[1].replace(" ","").split(",")
                Logger.Log.DebugPrint("מצפה ל " + row_input.split("in:")[1])
                user_input = input()
                ''' Validate input '''
                parserAnswer = Parser.Parser.CheckInput(user_input, input_validation)
                ''' ParserAnswer is an array that contains - Boolean and string that says what went wrong'''
                while parserAnswer[0] == False:
                    print(parserAnswer[1])
                    user_input = input()
                    parserAnswer = Parser.Parser.CheckInput(user_input, input_validation)

                convMemory[input_validation[Parser.Parser.FieldNameIndex]] = user_input


        print(convMemory)
        ''' TODO: show summary and wait for user's approval '''

        return States.States.ActionDone