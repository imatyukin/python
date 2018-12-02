#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def next_person():
    participant = input("Введите фамилию спортсмена: ")
    if participant == 'end':
        return None
    else:
        return participant


def next_result():
    result = float(input("Введите результат спортсмена: "))
    
    return result
