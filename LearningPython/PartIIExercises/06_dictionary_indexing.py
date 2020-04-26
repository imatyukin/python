#!/usr/bin/env python3

D = {'а': 1, 'Ь': 2, 'с': 3}
print(D['а'])               # 1
try:
    D['d']                  # KeyError: 'd'
except KeyError:
    print("KeyError: 'd'")
D['d'] = 'spam'             # {'а': 1, 'Ь': 2, 'с': 3, 'd': 'spam'}
print(D)
L = [0, 1]
try:
    L[2]                    # IndexError: list index out of range
except IndexError:
    print("IndexError: list index out of range")
try:
    L[2] = 3                # IndexError: list assignment index out of range
except IndexError:
    print("IndexError: list assignment index out of range")
