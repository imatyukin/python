#!/usr/bin/env python3

with open('james.txt') as jaf:
    data = jaf.readline()
james = data.strip().split(',')

with open('julie.txt') as juf:
    data = juf.readline()
julie = data.strip().split(',')

with open('mikey.txt') as mif:
    data = mif.readline()
mikey = data.strip().split(',')

with open('sarah.txt') as saf:
    data = saf.readline()
sarah = data.strip().split(',')
    
print(james)
print(julie)
print(mikey)
print(sarah)

print('\n================================ RESTART ================================\n')

print(sorted(james))
print(sorted(julie))
print(sorted(mikey))
print(sorted(sarah))

print('\n================================ RESTART ================================\n')

data = [6, 3, 1, 2, 4, 5]
print(data)

data.sort() # In-place sorting
print(data)

data = [6, 3, 1, 2, 4, 5]
data2 = sorted(data)    # Copied sorting
print(data2)
print(data)
