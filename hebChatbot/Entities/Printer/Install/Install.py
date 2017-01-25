import webbrowser
import socket
from uuid import getnode as get_mac
#import urllib

class Install:

    def __init__(self):
        self.mac = get_mac()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.host = socket.gethostname()
    def openExe(self):
        webbrowser.open('http://download.winzip.com/gl/nkln/winzip21.exe')

    def showInfo(self):
        print self.mac,self.ip,self.host
