#!/usr/bin/env python3

import os
os.chdir('/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter3')
print(os.getcwd())

data = open('sketch.txt')
print(data.readline(), end='')
print(data.readline(), end='')

data.seek(0)
for each_line in data:
    print(each_line, end='')

data.close()