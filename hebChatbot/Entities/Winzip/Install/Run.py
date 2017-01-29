import webbrowser
import socket
from uuid import getnode as get_mac
import os
import subprocess

def run(dict):
    mac = get_mac()
    ip = socket.gethostbyname(socket.gethostname())
    host = socket.gethostname()
    webbrowser.open('http://download.winzip.com/gl/nkln/winzip21.exe')
    file = 'C:\\Users\\User2\\Downloads\\winzip21.exe'
    subprocess.call([file], shell=True)
    print('printer installation')
    print(mac, ip, host)