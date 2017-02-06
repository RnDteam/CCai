''' Parser class
it expects the conversation file of each action would follow basic rule:
    input line would be in: שם-שדה,טיפוס-נתונים,אורך-קלט
    example like -   in: מספר-אישי,מספר,5
'''
class Parser():
    FieldNameIndex = 0
    InputTypeIndex = 1
    InputLengthIndex = 2

    @staticmethod
    def CheckInput(user_input, input_validation):
        ''' Check if all fields exist '''
        if len(input_validation) > Parser.InputLengthIndex:
            ''' check length '''
            if str(len(str(user_input))) == input_validation[Parser.InputLengthIndex]:
                return Parser.CheckType(user_input, input_validation)
            else:
                return [False, "אורך הקלט לא הגיוני, נסה שוב"]
        elif len(input_validation) > Parser.InputTypeIndex:
            return Parser.CheckType(user_input, input_validation)
        else:
            return [True, ""]

    @staticmethod
    def CheckType(user_input, input_validation):
        answer = [True, ""]

        ''' check type - there might be a cleaner way of doing it '''
        if input_validation[Parser.InputTypeIndex] == "מספר":
            if Parser.isNumeric(user_input):
                answer[0] = True
            else:
                answer[0] = False
                answer[1] = "מצטער, ציפיתי למספר."
        elif input_validation[Parser.InputTypeIndex] == "טקסט":
            ''' TODO: what verification do we need for text? '''
            answer[0] = True

        return answer

    @staticmethod
    def isNumeric(user_input):
        try:
            float(user_input)
        except:
            return False
        else:
            return True

class ParserInput():
    def __init__(self, args):
        self.fieldName = args[Parser.FieldNameIndex]
        if len(args) > Parser.InputTypeIndex:
            self.dataType = args[Parser.InputTypeIndex]
        if len(args) > Parser.InputLengthIndex:
            self.length = args[Parser.InputLengthIndex]

    def toArray(self):
        return [self.fieldName, self.dataType, self.length]