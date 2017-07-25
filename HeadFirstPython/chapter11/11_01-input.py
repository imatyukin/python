#!/usr/bin/env python3

res = input('What is your favorite programming language: ')
print(res)

age = input('What is your age: ')
print(type(age))
print(type(int(age)))

print('\n================================ RESTART ================================\n')

from find_it import find_closest

a = find_closest(3.3, [1.5, 2.5, 4.5, 5.2, 6])
print(a)

b = find_closest(3, [1, 5, 6])
print(b)

c = find_closest(3, [1, 3, 4, 6])
print(c)

d = find_closest(3.6, [1.5, 2.5, 4.5, 5.2, 6])
print(d)

e = find_closest(3, [1, 4, 6])
print(e)

f = find_closest(2.6, [1.5, 2.5, 4.5, 5.2, 6])
print(f)

print('\n================================ RESTART ================================\n')

from find_it import find_closest
from tm2secs2tm import time2secs, secs2time

def find_nearest_time(look_for, target_data):
    what = time2secs(look_for)
    where = [time2secs(t) for t in target_data]
    res = find_closest(what, where)
    return(secs2time(res))

a = find_nearest_time('59:59', ['56:29', '57:45', '59:03', '1:00:23', '1:01:45'])
print(a)

b = find_nearest_time('1:01:01', ['56:29', '57:45', '59:03', '1:00:23', '1:01:45'])
print(b)

c = find_nearest_time('1:02:01', ['56:29', '57:45', '59:03', '1:00:23', '1:01:45'])
print(c)

d = find_nearest_time('57:06', ['56:29', '57:45', '59:03', '1:00:23', '1:01:45'])
print(d)