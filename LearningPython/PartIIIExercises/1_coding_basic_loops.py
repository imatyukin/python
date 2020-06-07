#!/usr/bin/env python3

S = 'spam'
sum = 0
L = []
for c in S:
    print(c, '->', ord(c))
    sum += ord(c)
    L.append(ord(c))
print('sum = ', sum)
print(L)

print(list(map(ord, S)))
print([ord(c) for c in S])
