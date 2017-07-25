#!/usr/bin/env python3

import sys
sys.path.insert(0, r'/Users/igor/Documents/workspace/python3/HeadFirstPython')
from HeadFirstPython.chapter5.sanitize import sanitize

def get_coach_data_ver2(filename):
    try:
        with open(filename) as f:
            data = f.readline()
            templ = data.strip().split(',')
            return({'Name' : templ.pop(0),
                    'DOB' : templ.pop(0),
                    'Times': str(sorted(set([sanitize(t) for t in templ]))[0:3])})
    except IOError as ioerr:
        print('File error: ' + str(ioerr))
        return(None)