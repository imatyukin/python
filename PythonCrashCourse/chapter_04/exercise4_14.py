#!/usr/bin/env python3

import subprocess
import webbrowser
import sys

url = 'https://python.org/dev/peps/pep-0008/'
if sys.platform == 'darwin':    # in case of OS X
    subprocess.Popen(['open', url])
else:
    webbrowser.open_new_tab(url)