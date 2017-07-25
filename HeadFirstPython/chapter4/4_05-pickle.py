#!/usr/bin/env python3

import pickle

import os
data = open(os.path.join('/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter3', "sketch.txt"), "r")

import sys
sys.path.insert(0, '/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter2')
import nester

man = []
other = []
new_man = []

with open('mydata.pickle', 'wb') as mysavedata:
    pickle.dump([1, 2, 'three'], mysavedata)

with open('mydata.pickle', 'rb') as myrestoredata:
    a_list = pickle.load(myrestoredata)
    print(a_list)

print('\n================================ RESTART ================================\n')

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
    with open('man_data.txt', 'wb') as man_file, open('other_data.txt', 'wb') as other_file:
        pickle.dump(man, man_file)
        pickle.dump(other, other_file)
except IOError as err:
    print('File error: ' + str(err))
except pickle.PickleError as perr:
    pickle.dump(man, man_file)
    pickle.dump(other, other_file)
    print('Pickling error: ' + str(perr))
    
with open('man_data.txt', 'rb') as mdf:
    m_data = pickle.load(mdf)
    print(m_data)
    
print('\n================================ RESTART ================================\n')

try:
    with open('man_data.txt', 'rb') as man_file:
        new_man = pickle.load(man_file)
except IOError as err:
    print('File error: ' + str(err))
except pickle.PickleError as perr:
    print('Pickling error: ' + str(perr))
nester.print_lol(new_man)

print('\n================================ RESTART ================================\n')

print(new_man[0])
print(new_man[-1])