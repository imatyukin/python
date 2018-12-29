#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import jinja2
from .NakPos import NakPos


class Nakladnaya(object):

    TEMPLATE_LOADER = jinja2.PackageLoader('docs')
    TEMPLATE_ENVIRONMENT = jinja2.Environment(loader=TEMPLATE_LOADER)

    def __init__(self, number, created=None):
        self.__number = number
        if created is None:
            self.__created = datetime.now()
        else:
            self.__created = created
        self.__subscribed = False
        self.__contents = []

    @property
    def address(self):
        if self.__address is None:
            return 'Самовывоз'
        return self.__address

    @address.setter
    def address(self, new_addr):
        # @TODO Тут написать в лог, что адрес доставки изменился
        self.__address = new_addr
        
    @address.deleter
    def address(self):
        # @TODO Записать в лог, что адрес сброшен
        del self.__address

    @property
    def number(self):
        return self.__number

    @property
    def created(self):
        return self.__created

    @property
    def template(self):
        return Nakladnaya.TEMPLATE_ENVIRONMENT.get_template('nakladnaya.jinja2')

    @property
    def _contents(self):
        return iter(self.__contents)

    def print_paper(self):
        print(self.__number)
        print(self.__created)

    def subscribe(self):
        self.__subscribed = True

    def show(self):
        result = self.template.render(x=self)
        print(result)
    
    def add_pos(self, title, *, quantity=None, price=None, summa=None, **kwargs):
        pos = NakPos(title, quantity, price, summa)
        self.__contents.append(pos)

    def send(self):
        raise NotImplementedError()

    def __str__(self):
        num = self.__number
        dat = self.__created.strftime('%Y.%m.%d %H:%M')
        s = '*' if self.__subscribed else ' '
        return f'{s} {num} -- {dat}'








