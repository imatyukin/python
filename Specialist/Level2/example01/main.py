#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Glass import Glass


x = Glass()
# print(x.grad)
x.add_water(3)
x.add_alcohol(2)
print(x.vol, x.grad)
x.take(1.5)
print(x.vol, x.grad)
