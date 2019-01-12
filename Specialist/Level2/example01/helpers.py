#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def is_positive(func):
    def checked(self, x):
        if x <= 0:
            raise ValueError('Value must be positive')
        return func(self, x)
    return checked


# Это можно, но почти никогда не нужно
def force_float(func):
    def forced(self, x):
        return func(self, float(x))
    return forced