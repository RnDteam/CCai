import webbrowser
new = 2 # open in a new tab, if possible

# open a public URL, in this case, the webbrowser docs
url = "https://support.office.com/en-us/article/" \
      "Create-an-Outlook-Data-File-pst-to-save-your-information-17a13ca2-df52-48e8-b933-4c84c2aabe7c"


def run(dict, str_by_ref):
    str_by_ref[0] += '<a href=' + url + '>Pst in outlook</a>\n'
    # webbrowser.open(url, new=new)