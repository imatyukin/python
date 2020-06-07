#!/usr/bin/env python3

L = [1, 2, 4, 8, 16, 32, 64]
X = 5
found = False
i = 0
while not found and i < len(L):
    if 2 ** X == L[i]:
        found = True
    else:
        i = i + 1
    if found:
        print('at index', i)
    else:
        print(X, 'not found')

print('# a')

i = 0
while 2 ** X != L[i] and i < len(L):
        i += 1
        print(X, 'not found')
else:
    print('at index', i)

print('# b')

i = 0
for i in L:
    idx = L.index(i)
    if 2 ** X == L[idx]:
        print('at index', idx)
        break
    else:
        print(X, 'not found')

print('# c')

if 2 ** X in L:
    print('at index', L.index(2 ** X))
else:
    print(X, 'not found')

print('# d')

L = []
for i in range(7):
    L.append(2 ** i)
print(L)
if (2 ** X) in L:
    print('at index', L.index(2 ** X))
else:
    print(X, 'not found')

print('# f')

L = list(map(lambda x: 2 ** x, range(7)))     # Or [2 ** x for x in range(7)]
print(L)
if (2 ** X) in L:
    print('at index', L.index(2 ** X))
else:
    print(X, 'not found')
