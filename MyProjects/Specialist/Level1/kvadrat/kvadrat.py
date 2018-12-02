#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

a = input('a: ')
a = float(a)
b = input('b: ')
b = float(b)
c = input('c: ')
c = float(c)

D = b*b - 4.0*a*c

if D >= 0.0:
    x1 = ( -b - math.sqrt(D) ) / ( 2.0 * a )
    x2 = ( -b + math.sqrt(D) ) / ( 2.0 * a )
    print(x1, x2)
else:
    print('No solutions')

print('END')
