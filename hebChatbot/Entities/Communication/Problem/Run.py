import webbrowser
import socket
from uuid import getnode as get_mac
import os
import subprocess
import fileinput
import time

def run(dict):
    millis = int(round(time.time() * 1000))
    mac = get_mac()
    ip = socket.gethostbyname(socket.gethostname())
    host = socket.gethostname()
    file = open(os.path.join(os.path.dirname(__file__).split("hebChatbot")[0], "MashalWeb/main.html"), "r+",
                encoding='utf-8')
    newFile = open(os.path.join(os.path.dirname(__file__).split("hebChatbot")[0], "MashalWeb/main" + str(millis) +".html"), 'w',
                encoding = 'utf-8')
    myLine = ""
    for line in file:
        myLine = line
        for key in dict:
            if line.find(key) > -1:
                myLine = line.replace(key, dict[key])
        newFile.write(myLine)
    file.close()
    newFile.close()

    webbrowser.open('file://' + os.path.join(os.path.dirname(__file__).split("hebChatbot")[0],
                                             "MashalWeb/main" + str(millis) +".html"))
    print (mac,ip,host)