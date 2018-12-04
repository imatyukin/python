#!/usr/bin/env python3
# 1. Modify the Point class (from Shape.py or ShapeAlt.py), to support the
#    following operations, where p, q, and r are Points and n is a number:
#
#        p = q + r   # Point.__add__()
#        p += q      # Point.__iadd__()
#        p = q - r   # Point.__sub__()
#        p -= q      # Point.__isub__()
#        p = q * n   # Point.__mul__()
#        p *= n      # Point.__imul__()
#        p = q / n   # Point.__truediv__()
#        p /= n      # Point.__itruediv__()
#        p = q // n  # Point.__floordiv__()
#        p //= n     # Point.__ifloordiv__()
#
#    The in-place methods are all four lines long, including the def line, and
#    the other methods are each just two lines long, including the def line,
#    and of course they are all very similar and quite simple. With a minimal
#    description and a doctest for each it adds up to around one hundred thirty
#    new lines. A model solution is provided in Shape_ans.py; the same code is
#    also in ShapeAlt_ans.py.

import math


class Point:

    def __init__(self, x=0, y=0):
        """
        Метод инициализации (self - ссылка на сам объект)
        A 2D cartesian coordinate

        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x                      # переменной экземпляра self.x присваивается значение параметра x
        self.y = y                      # переменной экземпляра self.y присваивается значение параметра y

    def distance_from_origin(self):
        """
        Метод, выполняющий вычисления на основе переменных экземпляра объекта
        Returns the distance of the point from the origin

        >>> point = Point(3, 4)
        >>> point.distance_from_origin()
        5.0
        """
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        """
        Специальный метод __eq__(self, other)
        Пример использования x == y
        Возвращает True, если x равно y
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """
        Специальный метод __repr__(self)
        Пример использования repr(x)
        Возвращает строку с репрезентативной формой представления x, которая обеспечивает равенство eval(repr(x)) == x
        """
        return f'Point({self.x!r}, {self.y!r})'

    def __str__(self):
        """
        Специальный метод __str__(self)
        Пример использования str(x)
        Возвращает строковое представление x, пригодное для восприятия человеком
        """
        return f'({self.x!r}, {self.y!r})'


# Использование класса Point
a = Point()
print(repr(a))                          # вернёт: 'Point(0, 0)'
b = Point(3, 4)
print(str(b))                           # вернёт: '(3, 4)'
print(b.distance_from_origin())         # вернёт: 5.0
b.x = -19
print(str(b))                           # вернёт: '(-19, 4)'
print(a == b, a != b)                   # вернёт: False True
