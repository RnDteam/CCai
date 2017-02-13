import webbrowser
import socket
from uuid import getnode as get_mac
import os
import subprocess
import fileinput
import time
from MashalRequest import OpenMashal

problem_reason = "פניה ישירה"

def run(dict, str_by_ref):
    if not "סיבת-פניה" in dict:
        dict["סיבת-פניה"] = problem_reason

    OpenMashal.open_mashal(dict, str_by_ref, problem_reason)