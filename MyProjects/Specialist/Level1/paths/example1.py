#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import abspath, normpath, join

cwd = abspath('.')
print(cwd)

filename = join(cwd, 'file.txt')
print(filename)

parent = join(cwd, '..')
parent = normpath(parent)
print(parent)