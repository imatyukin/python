#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from weakref import ref


class MyComponent(object):

    def __init__(self, name, owner):
        self.name = name # жульничество, но пока можно
        self.__owner = owner
        owner._add_component(self)

    @property
    def owner(self):
        return self.__owner

    def __del__(self):
        print('Component', self.name, 'deleted')
