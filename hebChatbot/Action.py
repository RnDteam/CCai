import States as States
import Logger as Logger
import Parser as Parser
import UserStatus as UserStatus

yes_no_str_buttons = "[כן|לא]"
check_string = "חזרה"

class Action:
    def __init__(self, rootDir, entityName, actionName, spellingFileName, conversationFileName, entityNameHeb):
        self.rootDir = rootDir
        self.entityName = entityName
        self.actionName = actionName
        self.entityNameHeb = entityNameHeb
        self.spellingFileName = spellingFileName
        self.conversationFileName = conversationFileName
        self.check_line_index = 0
        self.spelling = []
        self.conversation = []
        
        self.init_spelling_bank()
        self.init_conversation()
        self.find_check_line()

    def init_spelling_bank(self):
        file = open(self.rootDir + '/' + self.entityName + '/' + self.actionName + '/' + self.spellingFileName, encoding='utf-8')
        self.spelling = [line.rstrip('\n') for line in file]
        self.actionNameHeb = self.spelling[0]

    def init_conversation(self):
        file = open(self.rootDir + '/' + self.entityName + '/' + self.actionName + '/' + self.conversationFileName,
                    encoding='utf-8')
        self.conversation = [line.rstrip('\n') for line in file]

    def find_check_line(self):
        for line_index in range(len(self.conversation)):
            if self.conversation[line_index].find(check_string) > -1:
                self.check_line_index = line_index
                return

    def StartConversation(self, user, message):
        str_to_print = ""

        if user.row_index < len(self.conversation):
            row_input = self.conversation[user.row_index]

            if user.is_mistaken:
                user.is_mistaken = False
                str_to_print += "בסדר, זה אנושי לטעות."

            ''' Detect if input or output '''
            if row_input.find("out:") > -1:
                ''' A output row might have a variable in it
                but as we create a parser class we would implement that'''
                str_to_print += row_input.split("out:")[1]
                user.is_asked_yes_no_question = row_input.find(yes_no_str_buttons) > -1

                while user.row_index < len(self.conversation) - 1 and row_input.find("out:") > -1:
                    user.is_asked_yes_no_question = row_input.find(yes_no_str_buttons) > -1
                    user.row_index += 1
                    row_input = self.conversation[user.row_index]

                    if row_input.find(check_string) > -1:
                        user.row_index += 1
                        row_input = self.conversation[user.row_index]

                    if row_input.find("out:") > -1:
                        str_to_print += '\n' + row_input.split("out:")[1]

                if user.row_index < len(self.conversation):
                    if row_input.find("in:") > -1:
                        input_validation = row_input.split("in:")[1].replace(" ", "").split(",")
                        ''' Checking if the input we need has already been given '''
                        if input_validation[Parser.Parser.FieldNameIndex] in user.convMemory:
                            ''' Ask if our memory value refers to him '''
                            str_to_print += "\nהאם זה " + user.convMemory[input_validation[Parser.Parser.FieldNameIndex]] + "\n"
                            str_to_print += yes_no_str_buttons
                            user.is_input_already_known = True
                            user.is_mistaken = False
                    else:
                        str_to_print = EndConversation(user, message, [str_to_print])
                    return str_to_print
                else:
                    str_to_print = EndConversation(user, message, [str_to_print])

            elif row_input.find("in:") > -1:
                input_validation = row_input.split("in:")[1].replace(" ", "").split(",")
                Logger.Log.DebugPrint("מצפה ל " + row_input.split("in:")[1])

                # This part handles if the user is denying to continue with the action
                if user.is_asked_yes_no_question and not user.is_input_already_known and UserStatus.IsDenied(message):
                    user.is_asked_yes_no_question = False
                    str_to_print = EndConversation(user, message, [str_to_print])
                    return str_to_print
                elif user.is_asked_yes_no_question and not user.is_input_already_known and not UserStatus.IsApproved(message):
                    user.row_index -= 1
                    return self.StartConversation(user, message)
                    # return "לא הצלחתי להבין אותך.\n האם ברצונך שאמשיך עם תהליך" + self.intent_name_heb() + "\n" + yes_no_str_buttons

                if not user.is_wrong_input:
                    ''' Checking if user is being mistaken '''
                    if UserStatus.IsMistaken(message):
                        ''' If it is the first input, then the user was wrong about the action '''
                        if user.index_input_arr == 0:
                            user.CURRENT_STATE = States.States.IntentRecognition
                            user.is_clear = False
                            user.row_index = 0
                            user.is_mistaken = True
                            return str_to_print
                        else:
                            user.is_mistaken = True

                            ''' go back to last input '''
                            prevInput = user.inputs_arr[user.index_input_arr - 1]
                            user.row_index = prevInput[0] - 1
                            user.index_input_arr -= 1
                            return self.StartConversation(user, message)
                            # return str_to_print
                            # continue

                    if user.is_input_already_known:
                        user.is_input_already_known = False
                        if UserStatus.IsApproved(message):
                            message = user.convMemory[input_validation[Parser.Parser.FieldNameIndex]]
                        elif UserStatus.IsDenied(message):
                            str_to_print += "אוקיי בבקשה הזן מחדש\n"
                            return str_to_print
                    ''' Saving input in an input dict '''
                    if len(user.inputs_arr) == user.index_input_arr:
                        user.inputs_arr.append([])

                    user.inputs_arr[user.index_input_arr] = [user.row_index, Parser.ParserInput(input_validation)]
                    user.index_input_arr += 1

                ''' Validate input '''
                parserAnswer = Parser.Parser.CheckInput(message, input_validation)
                ''' ParserAnswer is an array that contains - Boolean and string that says what went wrong'''
                if not parserAnswer[0]:
                    user.is_wrong_input = True
                    str_to_print += parserAnswer[1]
                    return str_to_print

                user.is_wrong_input = False

                if len(input_validation) > Parser.Parser.InputTypeIndex:
                    user.is_input_saved = True
                    user.convMemory[input_validation[Parser.Parser.FieldNameIndex]] = message
                user.row_index += 1
                return self.StartConversation(user, message)
            # Got all data and now confirms it
            elif row_input.find("אימות") > -1:
                if user.is_input_saved and not user.is_approve_details:
                    str_to_print += "אימות פרטים:\n"
                    for inputObj in user.inputs_arr:
                        if inputObj[1].fieldName in user.convMemory:
                            str_to_print += inputObj[1].fieldName.replace("-", " ") + ": " + "\n"
                            str_to_print += user.convMemory[inputObj[1].fieldName] + "\n"
                    str_to_print += "האם פרטיך נכונים?" + '\n' + yes_no_str_buttons
                    user.is_approve_details = True
                    user.is_asked_yes_no_question = True
                    return str_to_print
                elif user.is_input_saved and user.is_approve_details:
                    ''' TODO: change this later - it goes through all conversation again '''
                    if UserStatus.IsDenied(message) or UserStatus.IsMistaken(message):
                        user.inputs_arr = []
                        user.row_index = self.check_line_index + 1
                        user.index_input_arr = 0
                        user.is_mistaken = False
                        user.is_input_saved = False
                        user.is_input_already_known = False
                        user.is_approve_details = False
                        return self.StartConversation(user, message)
                    elif not UserStatus.IsApproved(message):
                        return "לצערי לא הבנתי. פרטיך נכונים?"
                    user.is_input_saved = False
                if user.is_approve_details or not user.is_input_saved:
                    str_to_print = EndConversation(user, message, [str_to_print])
            elif row_input.find(check_string) > -1:
                user.row_index += 1
        else:
            str_to_print = EndConversation(user, message, [str_to_print])

        return str_to_print

    def intent_name_heb(self):
        return self.entityNameHeb + ' ' + self.actionNameHeb

def EndConversation(user, message, str_by_ref):
    if not UserStatus.IsDenied(message):
        str_by_ref[0] = ActionMethod(user, str_by_ref)
    user.CURRENT_STATE = States.States.ActionDone
    user.is_clear = True
    user.is_asked_yes_no_question = False

    return str_by_ref[0]

def ActionMethod(user, str_by_ref):
    path = 'Entities.' + user.CURRENT_ACTION.entityName + '.' + user.CURRENT_ACTION.actionName + '.Run'
    runMethod = __import__(path)
    exec("runMethod." + user.CURRENT_ACTION.entityName + '.' + user.CURRENT_ACTION.actionName + '.Run' + ".run(user.convMemory, str_by_ref)")
    return str_by_ref[0]