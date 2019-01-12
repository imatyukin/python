#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shelve
from textwrap import dedent
from docs import Nakladnaya
from net import DocServer
from threading import Thread
import pickle
from urllib.request import urlopen


class Application(object):

    def __init__(self):
        self.__current = None
        self.__all_docs = []
        self.__filename = 'data.dat'
        self.__server = DocServer(('',8000))
        self.__dispatch = {
            '1': self.set_address,
            '2': self.add_pos,
            'C': self.create_doc,
            'L': self.show_all,
            'P': self.show_current,
            'R': self.select_current,
            'S': self.send_to_subscribe,
            'W': self.save_all,
            'G': self.load_all,
            'X': self.close_current,
        }

    def get_user_command(self):
        if self.__current is None:
            print(dedent('''\
                C - Создать накладную
                L - Показать список накладных
                R - Выбрать накладную для работы
                D - Удалить накладную
                W - Сохранить все
                G - Перезагрузить все
                Q - Завершить работу'''))
        else:
            print(dedent('''\
                1 - Указать адрес доставки
                2 - Добавить позицию
                3 - Удалить позицию
                P - Показать на экране
                S - Передать на подпись
                T - Передать на отправку
                U - Подписать
                X - Завершить работу с данной накладной'''))
        result = input(': ')
        return result

    def run(self):
        thread = Thread(target=self.__server.serve_forever)
        thread.start()
        try:
            while True:
                while not self.__server.queue.empty():
                    x = self.__server.queue.get(block=False)
                    self.__all_docs.append(x)
                command = self.get_user_command()
                if command == 'Q':
                    break
                else:
                    try:
                        method = self.__dispatch[command]
                        method()
                    except KeyError:
                        print('Неверная команда')
        finally:
            self.__server.shutdown()
            thread.join()

    def create_doc(self):
        self.__current = Nakladnaya(input('Номер: '))
        self.__all_docs.append(self.__current)
        
    def show_current(self):
        self.__current.show()

    def close_current(self):
        self.__current = None
        
    def show_all(self):
        for k, item in enumerate(self.__all_docs):
            print(k, item)

    def select_current(self):
        try:
            index = input('Индекс: ')
            index = int(index)
            self.__current = self.__all_docs[index]
        except ( IndexError, ValueError ):
            print('Ошибка. Повторите ввод.')

    def add_pos(self):
        title = input('Наименование: ').strip()
        quantity = input('Количество: ').strip()
        price = input('Цена: ').strip()
        summa = input('Сумма: ').strip()
        quantity = None if quantity == '' else quantity
        price = None if price == '' else price
        summa = None if summa == '' else summa
        self.__current.add_pos(title, quantity=quantity, price=price, summa=summa)
        
    def save_all(self):
        with shelve.open(self.__filename) as db:
            for doc in self.__all_docs:
                db[doc.number] = doc
                
    def load_all(self):
        self.__all_docs = []
        with shelve.open(self.__filename) as db:
            for key in db.keys():
                self.__all_docs.append(db[key])
        
    def set_address(self):
        new_addr = input('Адрес: ').strip()
        if new_addr == '':
            self.__current.address = None
        else:
            self.__current.address = new_addr

    def send_to_subscribe(self):
        '''Отправка на подпись'''
        data = pickle.dumps(self.__current)
        with urlopen('http://10.10.118.43:8000/subscribe',data=data) as net:
            response = net.read().decode('utf-8')
        if response == 'OK':
            self.__all_docs.remove(self.__current)
            self.__current = None
