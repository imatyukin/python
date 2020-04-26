#!/usr/bin/env python3

L = [0, 1, 2, 3]

try:
    print(L[4])             # IndexError: list index out of range
except IndexError:
    print("IndexError: list index out of range")
print(L[-1000:100])         # [0, 1, 2, 3]
print(L[3:1])               # []
L[3:1] = ['?']; print(L)    # [0, 1, 2, '?', 3]
