#!/usr/bin/env python3

L = [1, 2, 3, 4]
L[2] = []; print(L)             # [1, 2, [], 4]
L[2:3] = []; print(L)           # [1, 2, 4]
del L[0]; print(L)              # [2, 4]
del L[1:]; print(L)             # [2]
try:
    L[1:2] = 1                  # TypeError: can only assign an iterable
except TypeError:
    print("TypeError: can only assign an iterable")
