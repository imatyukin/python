#!/usr/bin/env python3
# 2. Modify the Image.py class to provide a resize(width, height) method. If the
#    new width or height is smaller than the current value, any colors outside
#    the new boundaries must be deleted. If either width or height is None then
#    use the existing width or height. At the end, make sure you regenerate
#    the self.__colors set. Return a Boolean to indicate whether a change
#    was made or not. The method can be implemented in fewer than 20 lines
#    (fewer than 35 including a docstring with a simple doctest). A solution is
#    provided in Image_ans.py.

"""
This module provides the Image class which holds (x, y, color) triples
and a background color to provide a kind of sparse-array representation of
an image. A method to export the image in XPM format is also provided.

>>> import os
>>> import tempfile
>>> red = "#FF0000"
>>> blue = "#0000FF"
>>> img = os.path.join(tempfile.gettempdir(), "test.img")
>>> xpm = os.path.join(tempfile.gettempdir(), "test.xpm")
>>> image = Image(10, 8, img)
>>> for x, y in ((0, 0), (0, 7), (1, 0), (1, 1), (1, 6), (1, 7), (2, 1),
...             (2, 2), (2, 5), (2, 6), (2, 7), (3, 2), (3, 3), (3, 4),
...             (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4),
...             (5, 5), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1),
...             (7, 2), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 6),
...             (8, 7), (9, 0), (9, 7)):
...    image[x, y] = blue
>>> for x, y in ((3, 1), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
...             (6, 1)):
...    image[(x, y)] = red
>>> print(image.width, image.height, len(image.colors), image.background)
10 8 3 #FFFFFF
>>> border_color = "#FF0000" # red
>>> square_color = "#0000FF" # blue
>>> width, height = 240, 60
>>> midx, midy = width // 2, height // 2
>>> image = Image(width, height, img, "#F0F0F0")
>>> for x in range(width):
...     for y in range(height):
...         if x < 5 or x >= width - 5 or y < 5 or y >= height -5:
...             image[x, y] = border_color
...         elif midx - 20 < x < midx + 20 and midy - 20 < y < midy + 20:
...             image[x, y] = square_color
>>> print(image.width, image.height, len(image.colors), image.background)
240 60 3 #F0F0F0
>>> image.save()
>>> newimage = Image(1, 1, img)
>>> newimage.load()
>>> print(newimage.width, newimage.height, len(newimage.colors), newimage.background)
240 60 3 #F0F0F0
>>> image.export(xpm)
>>> image.thing
Traceback (most recent call last):
...
AttributeError: 'Image' object has no attribute 'thing'
>>> for name in (img, xpm):
...     try:
...         os.remove(name)
...     except EnvironmentError:
...         pass
"""

import os
import pickle

USE_GETATTR = False


# Объявления собственных исключений
class ImageError(Exception): pass


# Наследуют исключение ImageError
class CoordinateError(ImageError): pass


class LoadError(ImageError): pass


class SaveError(ImageError): pass


class ExportError(ImageError): pass


class NoFilenameError(ImageError): pass


class Image:
    """
    Класс Image хранит одно значение цвета для фона плюс те пиксели изображения, цвет которых отличается от цвета фона
    Реализация с помощью словаря, разреженного массива, каждый ключ которого представляет координаты (x, y),
    а значение определяет цвет в точке с этими координатами
    """

    def __init__(self, width, height, filename="",
                 background="#FFFFFF"):
        """An image represented as HTML-style color values
        (color names or hex strings) at (x, y) coordinates with any
        unspecified points assumed to be the background
        """
        self.filename = filename        # имя файла (необязательно, имеет значение по умолчанию)
        # Частные атрибуты
        self.__background = background  # цвет фона (необязательно, имеет значение по умолчанию)
        self.__data = {}    # ключами словаря являются координаты (x, y), а его значениями строки, обозначающие цвет
        self.__width = width    # ширина
        self.__height = height  # высота
        self.__colors = {self.__background} # инициализируется значением цвета фона -
                                            # в нём хранятся все уникальные значения цвета, присутствующие в изображении

    if USE_GETATTR:
        def __getattr__(self, name):
            """
            >>> image = Image(10, 10)
            >>> len(image.colors) == 1
            True
            >>> image.width == image.height == 10
            True
            >>> image.thing
            Traceback (most recent call last):
            ...
            AttributeError: 'Image' object has no attribute 'thing'
            """
            if name == "colors":
                return set(self.__colors)
            classname = self.__class__.__name__
            if name in frozenset({"background", "width", "height"}):
                return self.__dict__["_{classname}__{name}".format(
                    **locals())]
            raise AttributeError("'{classname}' object has no "
                                 "attribute '{name}'".format(**locals()))
    else:
        # Доступ к частным атрибутам с помощью свойств
        @property
        def background(self):
            return self.__background

        @property
        def width(self):
            return self.__width

        @property
        def height(self):
            return self.__height

        @property
        def colors(self):
            return set(self.__colors)

    def __getitem__(self, coordinate):
        """
        Специальный метод __getitem__(self, k)
        Пример использования y[k]
        Возвращает k-й элемент последовательности y или значение элемента с ключом k в отображении y

        Метод возвращает цвет пикселя с заданными координатами,
        когда вызывающая программа использует оператор доступа к элементам ([])

        Returns the color at the given (x, y) coordinate; this will
        be the background color if the color has never been set
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
                not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate), self.__background)

    def __setitem__(self, coordinate, color):
        """
        Специальный метод __setitem__(self, k, v)
        Пример использования y[k] = v
        Устанавливает k-й элемент последовательности y или значение элемента с ключом k в отображении y

        Получение значения цвета из указанных координат

        Sets the color at the given (x, y), coordinate
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
                not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)

    def __delitem__(self, coordinate):
        """
        Специальный метод __delitem__(self, k)
        Пример использования del y[k]
        Удаляет k-й элемент последовательности y или элемент с ключом k в отображении y

        Когда удаляется значение цвета для заданных координат, происходит назначение цвета фона для этих координат

        Deletes the color at the given (x, y) coordinate

        In effect this makes the coordinate's color the background color.
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
                not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate), None)

    def save(self, filename=None):
        """
        Сохранение изображения на диск
        Консервирование данных (преобразование в последовательность байтов или в строку)

        Saves the current image, or the one specified by filename

        If filename is specified the internal filename is set to it.
        """
        # Проверка наличия файла
        # Если объект Image был создан без указания имени файла и после этого имя файла не было установлено,
        # то при вызове метода save() необходимо явно указывать имя файла
        if filename is not None:
            self.filename = filename    # установка значения атрибута filename
        # Если текущее имя файла не задано, то возбуждается исключение
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            # Создание списка, в который добавляются данные объекта для сохранения,
            # включая словарь self.__data с элементами координаты-цвет
            data = [self.width, self.height, self.__background,
                    self.__data]
            # Открытие файла для записи в двоичном режиме
            fh = open(self.filename, "wb")
            # Вызов функции pickle.dump(), которая записывает данные объекта в файл
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)  # протокол 3 - компактный двоичный формат
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self, filename=None):
        """
        Загрузка изображения с диска

        Loads the current image, or the one specified by filename

        If filename is specified the internal filename is set to it.
        """
        # Определение имени файла, который требуется загрузить
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            # Файл должен быть открыт для чтения в двоичном режие
            fh = open(self.filename, "rb")
            # Операция чтения выполняется инструкцией pickle.load()
            # Объект data - это точная реконструкция сохранявшегося объекта, т.е. список содержащий
            # целочисленные значения ширины и высоты, строку с цветом фона и словарь с элементами координаты-цвет
            data = pickle.load(fh)
            # Распаковка кортежа для присваивания каждого элемента списка data соответсвующей переменной
            # Множество уникальных цветов реконструируется посредством создания множества всех цветов,
            # хранящихся в словаре, после чего в множество добавляется цвет фона
            (self.__width, self.__height, self.__background,
             self.__data) = data
            self.__colors = (set(self.__data.values()) |
                             {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def export(self, filename):
        """Exports the image to the specified filename
        """
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " +
                              os.path.splitext(filename)[1])

    def __export_xpm(self, filename):
        """Exports the image as an XPM file if less than 8930 colors are
        used
        """
        name = os.path.splitext(os.path.basename(filename))[0]
        count = len(self.__colors)
        chars = [chr(x) for x in range(32, 127) if chr(x) != '"']
        if count > len(chars):
            chars = []
            for x in range(32, 127):
                if chr(x) == '"':
                    continue
                for y in range(32, 127):
                    if chr(y) == '"':
                        continue
                    chars.append(chr(x) + chr(y))
        chars.reverse()
        if count > len(chars):
            raise ExportError("cannot export XPM: too many colors")
        fh = None
        try:
            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(
                self, count, len(chars[0])))
            char_for_colour = {}
            for color in self.__colors:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_colour[color] = char
            fh.write("/* pixels */\n")
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)
                    row.append(char_for_colour[color])
                fh.write('"{0}",\n'.format("".join(row)))
            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def resize(self, width=None, height=None):
        """
        Метод resize(width, height)
        Если новая ширина или высота меньше текущего значения, все цвета,
        оказавшиеся за пределами новых границ изображения, удаляются.
        Если в качестве нового значения ширины или высоты передаётся None,
        соответсвующее значение ширины или высоты остаётся без изменений.

        Resizes to the given dimensions; returns True if changes made

        If a dimension is None; keeps the original. Deletes all out of
        range points.

        >>> image = Image(10, 10)
        >>> for x, y in zip(range(10), range(10)):
        ...     image[x, y] = "#00FF00" if x < 5 else "#0000FF"
        >>> image.width, image.height, len(image.colors)
        (10, 10, 3)
        >>> image.resize(5, 5)
        True
        >>> image.width, image.height, len(image.colors)
        (5, 5, 2)
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    border_color = "#FF0000"  # красный
    square_color = "#0000FF"  # синий
    width, height = 240, 60
    midx, midy = width // 2, height // 2
    image = Image(width, height, "square_eye.img")
    for x in range(width):
        for y in range(height):
            if x < 5 or x >= width - 5 or y < 5 or y >= height - 5:
                image[x, y] = border_color
            elif midx - 20 < x < midx + 20 and midy - 20 < y < midy + 20:
                image[x, y] = square_color
    image.save()
    image.export("square_eye.xpm")