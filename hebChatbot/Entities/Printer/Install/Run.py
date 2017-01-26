import webbrowser
import socket
from uuid import getnode as get_mac
import os
import subprocess

def run():
    mac = get_mac()
    ip = socket.gethostbyname(socket.gethostname())
    host = socket.gethostname()
    webbrowser.open('http://download.winzip.com/gl/nkln/winzip21.exe')
    file = 'C:\\Users\\User2\\Downloads\\winzip21.exe'
    subprocess.call([file], shell=True)
    print ('printer inatallation')
    print (mac,ip,host)