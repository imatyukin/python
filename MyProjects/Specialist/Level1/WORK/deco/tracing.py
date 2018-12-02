#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def trace(function):
    def traced(*args, **kwargs):
        print(f'Функция {function.__name__} вызвана')
        result = function(*args, **kwargs)
        print(f'Функция {function.__name__} завершена')
        return result
    return traced
