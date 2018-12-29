#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def trace(func):
    def traced_func(*args, **kwargs):
        print(func.__name__)
        result = func(*args, **kwargs)
        return result
    return traced_func

@trace
def func1(x, y):
    return x + y

@trace
def func2(x, y, z):
    return x + y*z
    

d = func1(2, 3)
e = func2(4, 5, 6)
