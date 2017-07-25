#!/usr/bin/env python3

import os
data = open(os.path.join('/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter3', "sketch.txt"), "r")

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

print(man)
print(other)