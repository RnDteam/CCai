import os

def IsMistaken(user_input):
    return CheckIfWordInFile(user_input, os.path.dirname(__file__)
                             + '/' + "UserStatus" + '/' + "Mistake" + "/" + "Spelling.txt")

def IsApproved(user_input):
    return CheckIfWordInFile(user_input, os.path.dirname(__file__)
                             + '/' + "UserStatus" + '/' + "Approval" + "/" + "Spelling.txt")

def IsDenied(user_input):
    return CheckIfWordInFile(user_input, os.path.dirname(__file__)
                             + '/' + "UserStatus" + '/' + "Denial" + "/" + "Spelling.txt")

def CheckIfWordInFile(user_input, filePath):
    file = open(filePath, encoding='utf-8')
    spelling = [line.rstrip('\n') for line in file]

    # TODO find better way to detect sentiment
    if not len(user_input.split(" ")) > 2:
        for word in user_input.split(" "):
            if word in spelling:
                return True

    return False
