#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers import is_positive, force_float

class GlassIsEmpty(Exception): pass


class Glass(object):

    def __init__(self):
        self.__water = 0.0 # литры
        self.__alcohol = 0.0 # литры

    @is_positive
    @force_float # это баловство
    def add_water(self, vol: float) -> None :
        self.__water += vol

    #@is_positive
    def add_alcohol(self, vol):
        self.__alcohol += vol

    @is_positive
    def take(self, vol):
        if self.vol <= 0.0:
            raise GlassIsEmpty()
        alcohol = self.grad * vol
        water = vol - alcohol
        if water >= self.__water or alcohol >= self.__alcohol:
            water   = self.__water
            alcohol = self.__alcohol
        self.__water   -= water
        self.__alcohol -= alcohol
        return ( water, alcohol )

    @property
    def vol(self):
        result = self.__water + self.__alcohol
        return result

    @vol.setter
    def vol(self, new_val):
        raise Exception('Invalid action')

    @vol.deleter
    def vol(self):
        pass

    @property
    def grad(self):
        result = self.__alcohol / self.vol
        return result
