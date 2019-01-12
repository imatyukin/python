#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MyContainer(object):

    def __init__(self, name):
        self.__all_components = []
        self.name = name # жульничество

    def _add_component(self, component):
        self.__all_components.append(component)
        
    def __del__(self):
        print('Container', self.name, 'deleted')

