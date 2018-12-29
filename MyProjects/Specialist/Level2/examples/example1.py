#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class A(object):

    def __init__(self):
        self.__var1 = 5
        self.__var2 = 10
        self.var3 = 15

    @property
    def var1(self):
        return self.__var1

    @property
    def var2(self):
        return self.__var2

    @var2.setter
    def var2(self, new_var):
        self.__var2 = new_var
