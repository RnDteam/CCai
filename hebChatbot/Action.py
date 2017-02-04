import States as States
import Logger as Logger
import Parser as Parser
import UserStatus as UserStatus

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

    def StartConversation(self, user, message):
        file = open(self.rootDir + '/' + self.entityName + '/' + self.actionName + '/' + self.conversationFileName,
                    encoding='utf-8')
        self.conversation = [line.rstrip('\n') for line in file]

        str_to_print = ""

        if user.row_index < len(self.conversation):
            row_input = self.conversation[user.row_index]
            user.is_input_already_known = False

            if user.is_mistaken == True:
                user.is_mistaken = False
                str_to_print += "בסדר, זה אנושי לטעות."

            ''' Detect if input or output '''
            if row_input.find("out:") > -1:
                ''' A output row might have a variable in it
                but as we create a parser class we would implement that'''
                str_to_print += row_input.split("out:")[1]
                user.row_index += 1
                row_input = self.conversation[user.row_index]
                while user.row_index < len(self.conversation) and row_input.find("out:") > -1:
                    str_to_print += row_input.split("out:")[1]

                    user.row_index += 1
                    row_input = self.conversation[user.row_index]

                return str_to_print
            elif row_input.find("in:") > -1:
                input_validation = row_input.split("in:")[1].replace(" ", "").split(",")
                Logger.Log.DebugPrint("מצפה ל " + row_input.split("in:")[1])

                ''' Checking if the input we need has already been given '''
                if input_validation[Parser.Parser.FieldNameIndex] in user.convMemory:
                    ''' Ask if our memory value refers to him '''
                    user_input = input("האם זה " + UserStatus.UserMemory.convMemory[input_validation[Parser.Parser.FieldNameIndex]] + "\n")
                    is_input_already_known = True

                #else:
                #    user_input = input()

                ''' Checking if user is being mistaken '''
                if UserStatus.IsMistaken(message) or (UserStatus.IsDenied(message) and user.index_input_arr == 0 and user.is_input_already_known ==  False):
                    ''' If it is the first input, then the user was wrong about the action '''
                    if user.index_input_arr == 0:
                        user.CURRENT_STATE = States.States.IntentRecognition
                        return str_to_print
                    else:
                        user.is_mistaken = True

                        ''' go back to last input '''
                        prevInput = user.inputs_arr[user.index_input_arr - 1]
                        row_index = prevInput[0] - 1
                        user.index_input_arr -= 1
                        return str_to_print
                        # continue

                if user.is_input_already_known == True:
                    if UserStatus.IsApproved(user_input):
                        #user_input = user.convMemory[input_validation[Parser.Parser.FieldNameIndex]]
                        message = user.convMemory[input_validation[Parser.Parser.FieldNameIndex]]
                    elif UserStatus.IsDenied(user_input):
                        str_to_print = "אוקיי בבקשה הזן את המידע מחדש\n"
                        return  # ?
                    else:
                        str_to_print = "אוקיי בבקשה הזן את המידע מחדש\n"
                        return  # ?

                ''' Saving input in an input dict '''
                if len(user.inputs_arr) == user.index_input_arr:
                    user.inputs_arr.append([])

                user.inputs_arr[user.index_input_arr] = [user.row_index, Parser.ParserInput(input_validation)]
                user.index_input_arr += 1

                ''' Validate input '''
                parserAnswer = Parser.Parser.CheckInput(message, input_validation)

                ''' ParserAnswer is an array that contains - Boolean and string that says what went wrong'''
                while parserAnswer[0] == False:
                    print(parserAnswer[1])
                    user_input = input()
                    parserAnswer = Parser.Parser.CheckInput(user_input, input_validation)

                if len(input_validation) > Parser.Parser.InputTypeIndex:
                    user.is_input_saved = True
                    user.convMemory[input_validation[Parser.Parser.FieldNameIndex]] = message
            user.row_index += 1

        if user.row_index == len(self.conversation):
            if user.is_input_saved:
                print("אימות פרטים:\n")
                for inputObj in user.inputs_arr:
                    if inputObj[1].fieldName in UserStatus.UserMemory.convMemory:
                        print(inputObj[1].fieldName.replace("-", " ") + ": ")
                        print(UserStatus.UserMemory.convMemory[inputObj[1].fieldName])

                print("פרטיך נכונים?")
                user_input = input()

                ''' TODO: change this later - it goes through all conversation again '''
                if UserStatus.IsDenied(user_input):
                    return self.StartConversation()

                user.is_approve_details = True
                user.is_input_saved = False
            if user.is_approve_details:
                path = 'Entities.' + self.entityName + '.' + self.actionName + '.Run'
                runMethod = __import__("hebChatbot." + path)
                exec("runMethod." + path + ".run(user.convMemory)")
                user.CURRENT_STATE = States.States.ActionDone

        file.close()
        return str_to_print

