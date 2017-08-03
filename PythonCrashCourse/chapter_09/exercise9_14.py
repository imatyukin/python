#!/usr/bin/env python3
from random import randint

class Die():

    def __init__(self, sides=6):
        '''N-гранный кубик'''
        self.sides = sides

    def roll_die(self, throws):
        '''Вывод случайного числа от 1 до количества сторон кубика с иммитацией количества бросков'''
        nums = [randint(1, self.sides) for throw in range(0, throws)]
        return print(', '.join(str(x) for x in nums))

cube = Die(6)       # модель 6-гранного кубика
cube.roll_die(10)   # имитация 10 бросков кубика
cube = Die(10)      # модель 10-гранного кубика
cube.roll_die(10)   # имитация 10 бросков кубика
cube = Die(20)      # модель 20-гранного кубика
cube.roll_die(10)   # имитация 10 бросков кубика