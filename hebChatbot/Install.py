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
        webbrowser.open('http://download.winzip.com/gl/nkln/winzip21.exe')#ip host mac address
        #testfile = urllib.URLopener()
        #testfile.retrieve("http://download.winzip.com/gl/nkln/winzip21.exe", "f")

    def showInfo(self):
        print self.mac,self.ip,self.host

if __name__ == '__main__':
    inst = Install()
    inst.openExe()
    inst.showInfo()
"""

import mechanize
from time import sleep
#Make a Browser (think of this as chrome or firefox etc)
br = mechanize.Browser()

#visit http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/
#for more ways to set up your br browser object e.g. so it look like mozilla
#and if you need to fill out forms with passwords.

# Open your site
br.open('http://pypi.python.org/pypi/xlwt')

f=open("source.html","w")
f.write(br.response().read()) #can be helpful for debugging maybe

filetypes=[".exe"] #you will need to do some kind of pattern matching on your files
myfiles=[]
for l in br.links(): #you can also iterate through br.forms() to print forms on the page!
    for t in filetypes:
        if t in str(l): #check if this link has the file extension we want (you may choose to use reg expressions or something)
            myfiles.append(l)


def downloadlink(l):
    f=open(l.text,"w") #perhaps you should open in a better way & ensure that file doesn't already exist.
    br.click_link(l)
    f.write(br.response().read())
    print l.text," has been downloaded"
    #br.back()

for l in myfiles:
    sleep(1) #throttle so you dont hammer the site
    downloadlink(l)"""