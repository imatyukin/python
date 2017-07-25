#!/usr/bin/env python3

from sanitize import sanitize

with open('james.txt') as jaf: data = jaf.readline()
james = data.strip().split(',')
with open('julie.txt') as juf: data = juf.readline()
julie = data.strip().split(',')
with open('mikey.txt') as mif: data = mif.readline()
mikey = data.strip().split(',')
with open('sarah.txt') as saf: data = saf.readline()
sarah = data.strip().split(',')

clean_james = []
clean_julie = []
clean_mikey = []
clean_sarah = []

for each_t in james:
    clean_james.append(sanitize(each_t))
for each_t in julie:
    clean_julie.append(sanitize(each_t))
for each_t in mikey:
    clean_mikey.append(sanitize(each_t))
for each_t in sarah:
    clean_sarah.append(sanitize(each_t))
    
clean_james = [sanitize(each_t) for each_t in james]
clean_julie = [sanitize(each_t) for each_t in julie]
clean_mikey = [sanitize(each_t) for each_t in mikey]
clean_sarah = [sanitize(each_t) for each_t in sarah]

print(sorted(clean_james))
print(sorted(clean_julie))
print(sorted(clean_mikey))
print(sorted(clean_sarah))

print('\n================================ RESTART ================================\n')

print(sorted([sanitize(t) for t in james]))
print(sorted([sanitize(t) for t in julie]))
print(sorted([sanitize(t) for t in mikey]))
print(sorted([sanitize(t) for t in sarah]))

print('\n================================ RESTART ================================\n')

print(james[0])
print(james[1])
print(james[2])
print(james[0:3])

print('\n================================ RESTART ================================\n')

mins = [1, 2, 3]
secs = [m * 60 for m in mins]
print(secs)

print('\n================================ RESTART ================================\n')

meters = [1, 10, 3]
feet = [m * 3.281 for m in meters]
print(feet)

print('\n================================ RESTART ================================\n')

lower = ["I", "don't", "like", "spam"]
upper = [s.upper() for s in lower]
print(upper)

print('\n================================ RESTART ================================\n')

dirty = ['2-22', '2:22', '2.22']
clean = [sanitize(t) for t in dirty]
print(clean)

print('\n================================ RESTART ================================\n')

clean = [float(s) for s in clean]
print(clean)

print('\n================================ RESTART ================================\n')

clean = [float(sanitize(t)) for t in ['2-22', '3:33', '4.44']]
print(clean)

