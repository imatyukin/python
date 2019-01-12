#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decimal import Decimal


def _to_4(value):
    if value is None:
        return None
    return Decimal(value).quantize(Decimal('0.0001'))
    
def _to_2(value):
    if value is None:
        return None
    return Decimal(value).quantize(Decimal('0.01'))


class NakPos(object):

    def __init__(self, title, quantity=None, price=None, summa=None):
        self.__title = title
        self.__quantity = _to_4(quantity)
        self.__price    = _to_4(price)
        self.__summa    = _to_2(summa)

    @property
    def title(self):
        return self.__title

    @property
    def quantity(self):
        return self.__quantity

    @property
    def price(self):
        return self.__price

    @property
    def summa(self):
        if self.__summa is None:
            return _to_2(self.quantity * self.price)
        return self.__summa
