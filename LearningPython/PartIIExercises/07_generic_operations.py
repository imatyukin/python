#!/usr/bin/env python3

try:
    "х" + 1                     # TypeError: can only concatenate str (not "int") to str
except TypeError:
    print('TypeError: can only concatenate str (not "int") to str')
try:
    {} + {}                     # TypeError: unsupported operand type(s) for +: 'dict' and 'dict'
except TypeError:
    print("TypeError: unsupported operand type(s) for +: 'dict' and 'dict'")
print([].append(9))             # None
L = []; L.append(9); print(L)   # [9]
try:
    print(" ".append('s'))      # AttributeError: 'str' object has no attribute 'append'
except AttributeError:
    print("AttributeError: 'str' object has no attribute 'append'")
print(list({}.keys()))
try:
    [].keys()                   # AttributeError: 'list' object has no attribute 'keys'
except AttributeError:
    print("AttributeError: 'list' object has no attribute 'keys'")
print([][:])                    # []
print(""[:])                    # ''
