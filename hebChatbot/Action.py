import hebChatbot.States as States
import hebChatbot.Logger as Logger
import hebChatbot.Parser as Parser
import hebChatbot.UserStatus as UserStatus
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

        inputs_arr = []
        row_index = 0
        index_input_arr = 0
        isMistaken = False

        while row_index < len(self.conversation):
            row_input = self.conversation[row_index]
            if isMistaken == True:
                isMistaken = False
                print("בסדר, זה אנושי לטעות.")
            ''' We would prefer to have a parser class
             which handles the conversation file '''
            if row_input.startswith("out:"):
                ''' A output row might have a variable in it
                but as we create a parser class we would implement that'''
                print(row_input.split("out:")[1])
            elif row_input.startswith("in:"):
                input_validation = row_input.split("in:")[1].replace(" ", "").split(",")

                Logger.Log.DebugPrint("מצפה ל " + row_input.split("in:")[1])
                user_input = input()

                ''' Checking if user is being mistaken '''
                if UserStatus.IsMistaken(user_input):
                    ''' If it is the first input, then the user was wrong about the action '''
                    if index_input_arr == 0:
                        return States.States.IntentRecognition
                    else:
                        isMistaken = True

                        ''' go back to last input '''
                        prevInput = inputs_arr[index_input_arr - 1]
                        row_index = prevInput[0] - 1
                        index_input_arr -= 1
                        continue

                ''' Saving input in an input dict '''
                if len(inputs_arr) == index_input_arr:
                    inputs_arr.append([])

                inputs_arr[index_input_arr] = [row_index, Parser.ParserInput(input_validation)]
                index_input_arr += 1

                ''' Validate input '''
                parserAnswer = Parser.Parser.CheckInput(user_input, input_validation)

                ''' ParserAnswer is an array that contains - Boolean and string that says what went wrong'''
                while parserAnswer[0] == False:
                    print(parserAnswer[1])
                    user_input = input()
                    parserAnswer = Parser.Parser.CheckInput(user_input, input_validation)

                convMemory[input_validation[Parser.Parser.FieldNameIndex]] = user_input
            row_index += 1

        print(convMemory)
        ''' TODO: show summary and wait for user's approval '''
        path = 'Entities.' + self.entityName + '.' +self.actionName+'.Run'
        runMethod = __import__("hebChatbot."+path)
        exec("runMethod."+path+".run()")
        return States.States.ActionDone

