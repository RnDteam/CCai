import webbrowser
import subprocess

def run(dict, str_by_ref):
    str_by_ref[0] += "חבר הפנה אותך לקישור\n"
    webbrowser.open('http://download.winzip.com/gl/nkln/winzip21.exe')
    file = 'C:\\Users\\User2\\Downloads\\winzip21.exe'
    subprocess.call([file], shell=True)
