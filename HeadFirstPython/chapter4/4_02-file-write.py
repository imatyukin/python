#!/usr/bin/env python3

import os
data = open(os.path.join('/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter3', "sketch.txt"), "r")

out = open("data.out", "w")
print("Norwegian Blues stun easily.", file=out)
out.close()

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
    man_file = open('man_data.txt', 'w')
    other_file = open('other_data.txt', 'w')
    
    print(man, file=man_file)
    print(other, file=other_file)

except IOError:
    print('File error.')
    
finally:
    man_file.close()
    other_file.close()
