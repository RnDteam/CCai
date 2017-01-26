import os

def IsMistaken(user_input):
    file = open(os.path.dirname(__file__)  + '/' + "UserStatus" + '/' + "Mistake" + "/" + "Spelling.txt", encoding='utf-8')
    spelling = [line.rstrip('\n') for line in file]
    for word in user_input.split(" "):
        if word in spelling:
            return True

    return False
