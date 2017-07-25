#!/usr/bin/env python3

from get_coach_data import get_coach_data
from sanitize import sanitize

james = get_coach_data('james.txt')
julie = get_coach_data('julie.txt')
mikey = get_coach_data('mikey.txt')
sarah = get_coach_data('sarah.txt')

print(sorted(set([sanitize(t) for t in james]))[0:3])
print(sorted(set([sanitize(t) for t in julie]))[0:3])
print(sorted(set([sanitize(t) for t in mikey]))[0:3])
print(sorted(set([sanitize(t) for t in sarah]))[0:3])

print('\n================================ RESTART ================================\n')

unique_james = []
for each_t in james:
    if each_t not in unique_james:
        unique_james.append(each_t)
print(unique_james[0:3])

print('\n================================ RESTART ================================\n')

james = sorted([sanitize(t) for t in james])
print(james)
unique_james = []
[unique_james.append(t) for t in james if t not in unique_james]
print(unique_james[0:3])

print(sorted(set(james))[0:3])

julie = sorted([sanitize(t) for t in julie])
print(julie)
unique_julie = []
[unique_julie.append(t) for t in julie if t not in unique_julie]
print(unique_julie[0:3])

print(sorted(set(julie))[0:3])

mikey = sorted([sanitize(t) for t in mikey])
print(mikey)
unique_mikey = []
[unique_mikey.append(t) for t in mikey if t not in unique_mikey]
print(unique_mikey[0:3])

print(sorted(set(mikey))[0:3])

sarah = sorted([sanitize(t) for t in sarah])
print(sarah)
unique_sarah = []
[unique_sarah.append(t) for t in sarah if t not in unique_sarah]
print(unique_sarah[0:3])

print(sorted(set(sarah))[0:3])

print('\n================================ RESTART ================================\n')

distances = set()
distances = {10.6, 11, 8, 10.6, "two", 7}
print(distances)

print(james)
distances = set(james)
print(distances)

