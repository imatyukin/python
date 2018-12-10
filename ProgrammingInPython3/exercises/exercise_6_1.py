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

    def __add__(self, other):
        """
        Специальный метод __add__(self, other)
        Пример использования x + y
        Returns a new Point whose coordinate are the sum of this
        one's and the other one's

        >>> p = Point(1, 2)
        >>> q = p + Point(3, 4)
        >>> q
        Point(4, 6)
        """
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """
        Специальный метод __iadd__(self, other)
        Пример использования x += y
        Returns this Point with its coordinate set to the sum of this
        one's and the other one's

        >>> p = Point(1, 2)
        >>> p += Point(3, 4)
        >>> p
        Point(4, 6)
        """
        self.x += other.x
        self.y += other.y
        return Point(self.x, self.y)

    def __sub__(self, other):
        """
        Специальный метод __sub__(self, other)
        Пример использования x - y
        Returns a new Point whose coordinate are the difference of this
        one's and the other one's

        >>> p = Point(1, 2)
        >>> q = p - Point(3, 4)
        >>> q
        Point(-2, -2)
        """
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        """
        Специальный метод __isub__(self, other)
        Пример использования x -= y
        Returns this Point with its coordinate set to the difference
        of this one's and the other one's

        >>> p = Point(1, 2)
        >>> p -= Point(3, 4)
        >>> p
        Point(-2, -2)
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        """
        Специальный метод __mul__(self, other)
        Пример использования x * y
        Returns a new Point whose coordinate is this one's multiplied
        by the other number

        >>> p = Point(1, 2)
        >>> q = p * 3
        >>> q
        Point(3, 6)
        """
        return Point(self.x * other, self.y * other)

    def __imul__(self, other):
        """
        Специальный метод __imul__(self, other)
        Пример использования x *= y
        Returns this Point with its coordinate set to this one's
        multiplied by the other number

        >>> p = Point(1, 2)
        >>> p *= 3
        >>> p
        Point(3, 6)
        """
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other):
        """
        Специальный метод __truediv__(self, other)
        Пример использования x / y
        Returns a new Point whose coordinate is this one's divided
        by the other number

        >>> p = Point(1, 2)
        >>> q = p / 3
        >>> q
        Point(0.3333333333333333, 0.6666666666666666)
        """
        return Point(self.x / other, self.y / other)

    def __itruediv__(self, other):
        """
        Специальный метод __itruediv__(self, other)
        Пример использования x /= y
        Returns this Point with its coordinate set to this one's
        divided by the other number

        >>> p = Point(1, 2)
        >>> p /= 3
        >>> p
        Point(0.3333333333333333, 0.6666666666666666)
        """
        self.x /= other
        self.y /= other
        return self

    def __floordiv__(self, other):
        """
        Специальный метод __floordiv__(self, other)
        Пример использования x // y
        Returns a new Point whose coordinate is this one's floor
        divided by the other number

        >>> p = Point(1, 2)
        >>> q = p // 3
        >>> q
        Point(0, 0)
        """
        return Point(self.x // other, self.y // other)

    def __ifloordiv__(self, other):
        """
        Специальный метод __ifloordiv__(self, other)
        Пример использования x //= y
        Returns this Point with its coordinate set to this one's
        floor divided by the other number

        >>> p = Point(1, 2)
        >>> p //= 3
        >>> p
        Point(0, 0)
        """
        self.x //= other
        self.y //= other
        return self

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

# p, q и r являются объектами типа Point, а n - число

print("Поддержка операции p = q + r     # Point.__add__():")
p = Point(1, 2)
q = p + Point(3, 4)
print(q)                                # вернёт: '(4, 6)'
print("Поддержка операции p += q        # Point.__iadd__():")
p = Point(1, 2)
p += Point(3, 4)
print(p)                                # вернёт: '(4, 6)'
print("Поддержка операции p = q - r     # Point.__sub__():")
p = Point(1, 2)
q = p - Point(3, 4)
print(q)                                # вернёт: '(-2, -2)'
print("Поддержка операции p -= q        # Point.__isub__():")
p = Point(1, 2)
p -= Point(3, 4)
print(p)                                # вернёт: '(-2, -2)'
print("Поддержка операции p = q * n     # Point.__mul__():")
p = Point(1, 2)
q = p * 3
print(q)                                # вернёт: '(3, 6)'
print("Поддержка операции p *= n        # Point.__imul__():")
p = Point(1, 2)
p *= 3
print(p)                                # вернёт: '(3, 6)'
print("Поддержка операции p = q / n     # Point.__truediv__():")
p = Point(1, 2)
q = p / 3
print(q)                                # вернёт: '(0.3333333333333333, 0.6666666666666666)'
print("Поддержка операции p /= n        # Point.__itruediv__()")
p = Point(1, 2)
p /= 3
print(p)                                # вернёт: '(0.3333333333333333, 0.6666666666666666)'
print("Поддержка операции p = q // n  # Point.__floordiv__():")
p = Point(1, 2)
q = p // 3
print(q)                                # вернёт: '(0, 0)'
print("Поддержка операции p //= n     # Point.__ifloordiv__():")
p = Point(1, 2)
p //= 3
print(p)                                # вернёт: '(0, 0)'


if __name__ == "__main__":
    import doctest
    doctest.testmod()