#!/usr/bin/env python3

import os
import sys
import glob
import pickle
from athletemodel import get_from_store
from athletemodel import put_to_store

print(dir())

path = '/Users/igor/Documents/workspace/python3/HeadFirstPython/chapter6/*.txt'
the_files = glob.glob(path)
print(the_files)

data = put_to_store(the_files)
print(data)

for each_athlete in data:
    print(data[each_athlete].name + ' ' + data[each_athlete].dob)

data_copy = get_from_store()
for each_athlete in data_copy:
    print(data_copy[each_athlete].name + ' ' + data_copy[each_athlete].dob)
