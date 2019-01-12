#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tracing import trace


@trace
def func(x,y):
    print('x =', x)
    print('y =', y)
    return x+y

# @trace
def func2(x,y,z):
    print('Hello!')
    return x*y*z

    
z = func(2,3)
print(z)

func2(3,4,5)
