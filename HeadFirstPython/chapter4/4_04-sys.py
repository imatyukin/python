#!/usr/bin/env python3

import os
import sys

data = open(os.path.join('/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter3', "sketch.txt"), "r")

sys.path.insert(0, '/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter2')
import nester


man = []
other = []

try:    
    for each_line in data:
        try:
            (role, line_spoken) = each_line.split(':', 1)
            line_spoken = line_spoken.strip()
            if role == 'Man':
                man.append(line_spoken)
            elif role == 'Other Man':
                other.append(line_spoken)
        except ValueError:
            pass

    data.close()
except IOError:
    print('The datafile is missing!')

try:
    with open('man_data.txt', 'w') as man_file, open('other_data.txt', 'w') as other_file:
        print(man, file=man_file)
        print(other, file=other_file)
except IOError as err:
    print('File error: ' + str(err))
    
print('\n================================ RESTART ================================\n')

with open('man_data.txt') as mdf:
    print(mdf.readline())

try:
    with open('man_data.txt', 'w') as man_file, open('other_data.txt', 'w') as other_file:
        nester.print_lol(man, fh=man_file)
        nester.print_lol(other, fh=other_file)
except IOError as err:
    print('File error: ' + str(err))
    
with open('man_data.txt') as mdf:
    mdf.seek(0)
    for each_line in mdf:
        print(each_line, end='')