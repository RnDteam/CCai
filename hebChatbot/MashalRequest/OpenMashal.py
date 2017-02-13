import webbrowser
import socket
from uuid import getnode as get_mac
import os
import subprocess
import fileinput
import time

def open_mashal(dict, str_by_ref, problem_reason):
    millis = int(round(time.time() * 1000))
    mac = get_mac()
    ip = socket.gethostbyname(socket.gethostname())
    host = socket.gethostname()
    file = open(os.path.join(os.path.dirname(__file__).split("hebChatbot")[0], "MashalWeb/main.html"), "r+",
                encoding='utf-8')
    newFile = open(os.path.join(os.path.dirname(__file__).split("hebChatbot")[0], "MashalWeb/main" + str(millis) +".html"), 'w',
                encoding = 'utf-8')
    myLine = ""

    add_variables(dict)
    for line in file:
        myLine = line
        for key in dict:
            if line.find(key) > -1:
                myLine = line.replace(key, dict[key])
        newFile.write(myLine)
    file.close()
    newFile.close()
    remove_variables(dict)

    str_by_ref[0] += "מספר התקלה שפתחתי לך עבור " + problem_reason + " הוא:" + '\n'
    str_by_ref[0] += str(millis)[:9] + '\n'
    webbrowser.open('file://' + os.path.join(os.path.dirname(__file__).split("hebChatbot")[0],
                                             "MashalWeb/main" + str(millis) +".html"))
    print (mac,ip,host)

def add_variables(dict):
    millis = int(round(time.time() * 1000))

    dict["מספר-תקלה"] = str(millis)[:9]
def remove_variables(dict):
    dict.pop("מספר-תקלה", None)
    dict.pop("הסבר-בעיה", None)
    dict.pop("סיבת-פניה", None)