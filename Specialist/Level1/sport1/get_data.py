#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def next_person():
    fam = input('фамилия: ')
    if fam == 'end':
        return None
    res = input('результат: ')
    res = float(res)
    return ( res, fam, )


def coming():
    while True:
        res = next_person()
        if res is None:
            break
        yield res
