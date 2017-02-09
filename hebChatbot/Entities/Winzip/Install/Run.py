import webbrowser
import subprocess

url = 'http://download.winzip.com/gl/nkln/winzip21.exe'

def run(dict, str_by_ref):
    str_by_ref[0] += "הנה קישור להתקנה \n"
    str_by_ref[0] += '\n<a href=' + url + '>התקנת וינזיפ</a>\n'

    # webbrowser.open(url)
    # file = 'C:\\Users\\User2\\Downloads\\winzip21.exe'
    # subprocess.call([file], shell=True)
