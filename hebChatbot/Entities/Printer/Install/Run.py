from MashalRequest import OpenMashal

problem_reason = "התקנת מדפסת"

def run(dict, str_by_ref):
    dict["סיבת-פניה"] = problem_reason
    OpenMashal.open_mashal(dict, str_by_ref, problem_reason)