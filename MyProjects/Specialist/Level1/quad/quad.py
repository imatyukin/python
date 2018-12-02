#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

print('Решение квадратного уравнения:\n')

a = 0
while (a == 0):
    a = float(input("Введите a: "))
b = float(input("Введите b: "))
c = float(input("Введите c: "))

D = pow(b,2) - (4*a*c)

if D > 0:
    x1 = (-b + math.sqrt(D)) / (2*a*c)
    x2 = (-b - math.sqrt(D)) / (2*a*c)
    print("x1="+str(round(x1, 2)), "x2="+str(round(x2, 2)))
elif D == 0:
    x1 = -(b / (2*a))
    print("x1=x2="+str(x1))
else:
    print("Корней нет")

print('\nПрограмма завершена.')
input()