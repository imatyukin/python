#!/usr/bin/env python3

import sys
sys.path.insert(0, r'/Users/igor/Documents/workspace/python3/HeadFirstPython')
from HeadFirstPython.chapter5.sanitize import sanitize
from HeadFirstPython.chapter5.get_coach_data import get_coach_data
from get_coach_data_ver2 import get_coach_data_ver2

sarah = get_coach_data('sarah2.txt')
(sarah_name, sarah_dob) = sarah.pop(0), sarah.pop(0)
print(sarah_name + "'s fastest times are: " + str(sorted(set([sanitize(t) for t in sarah]))[0:3]))

print('\n================================ RESTART ================================\n')

sarah = get_coach_data('sarah2.txt')
sarah_data = {}
sarah_data['Name'] = sarah.pop(0)
sarah_data['DOB'] = sarah.pop(0)
sarah_data['Times'] = sarah
print(sarah_data['Name'] + "’s fastest times are: " + str(sorted(set([sanitize(t) for t in sarah_data['Times']]))[0:3]))

print('\n================================ RESTART ================================\n')

james = get_coach_data_ver2('james2.txt')
julie = get_coach_data_ver2('julie2.txt')
mikey = get_coach_data_ver2('mikey2.txt')
sarah = get_coach_data_ver2('sarah2.txt')

print(james['Name'] + "'s fastest times are: " + james['Times'])
print(julie['Name'] + "'s fastest times are: " + julie['Times'])
print(mikey['Name'] + "'s fastest times are: " + mikey['Times'])
print(sarah['Name'] + "'s fastest times are: " + sarah['Times'])
