#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def trace(function):
    def traced(*args, **kwargs):
        print(f'Function {function.__name__} called')
        result = function(*args, **kwargs)
        print(f'Function {function.__name__} completed')
        return result
    return traced
