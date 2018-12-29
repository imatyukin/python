#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import count
from weakref import WeakValueDictionary


class MyContainer(object):

    def __init__(self, name):
        self.__counter = count(0)
        self.__all_components = WeakValueDictionary()
        self.name = name # жульничество

    def _add_component(self, component):
        no = next(self.__counter)
        self.__all_components[no] = component
        
    def __del__(self):
        print('Container', self.name, 'deleted')
