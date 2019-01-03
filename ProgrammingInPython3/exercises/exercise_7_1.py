#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1. Make a new, simpler version of the BinaryRecordFile module—one that
#    does not use a state byte. For this version the record size specified by
#    the user is the record size actually used. New records must be added using
#    a new append() method that simply moves the file pointer to the end
#    and writes the given record. The __setitem__() method should only allow
#    existing records to be replaced; one easy way of doing this is to use the
#    __seek_to_index() method. With no state byte, __getitem__() is reduced to
#    a mere three lines. The __delitem__() method will need to be completely
#    rewritten since it must move all the records up to fill the gap; this can be
#    done in just over half a dozen lines, but does require some thought. The
#    undelete() method must be removed since it is not supported, and the compact()
#    and inplace_compact() methods must be removed because they are
#    no longer needed.
#    All told, the changes amount to fewer than 20 new or changed lines and
#    at least 60 deleted lines compared with the original, and not counting
#    doctests. A solution is provided in BinaryRecordFile_ans.py.

"""
>>> import shutil
>>> import sys

>>> S = struct.Struct("<15s")
>>> fileA = os.path.join(tempfile.gettempdir(), "fileA.dat")
>>> fileB = os.path.join(tempfile.gettempdir(), "fileB.dat")
>>> for name in (fileA, fileB):
...    try:
...        os.remove(name)
...    except EnvironmentError:
...        pass

>>> brf = BinaryRecordFile(fileA, S.size)
>>> for text in ("Alpha", "Bravo", "Charlie", "Delta",
...        "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
...        "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
...        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor",
...        "Whisky", "X-Ray", "Yankee", "Zulu"):
...    brf.append(S.pack(text.encode("utf8")))
>>> assert len(brf) == 26
>>> brf.append(S.pack(b"Extra at the end"))
>>> assert len(brf) == 27
>>> shutil.copy(fileA, fileB)
>>> del brf[12]
>>> del brf[0]
>>> del brf[24]
>>> assert len(brf) == 24, len(brf)
>>> brf.close()

>>> if ((os.path.getsize(fileA) + (3 * S.size)) !=
...        os.path.getsize(fileB)):
...    print("FAIL#1: expected file sizes are wrong")
...    sys.exit()

>>> shutil.copy(fileB, fileA)
>>> if os.path.getsize(fileA) != os.path.getsize(fileB):
...    print("FAIL#2: expected file sizes differ")
...    sys.exit()

>>> for name in (fileA, fileB):
...    try:
...        os.remove(name)
...    except EnvironmentError:
...        pass

"""

import os
import struct
import tempfile


class BinaryRecordFile:
    """Класс BinaryRecordFile, в котором не используется байт состояния записи.
    Размер записи, устанавливаемый пользователем, совпадает с истинным размером записи.
    """

    def __init__(self, filename, record_size, auto_flush=True):
        """Двоичный файл с произвольным доступом, который ведёт себя, как список,
        каждый элемент которого представляет собой bytes или bytesarray объект record_size.
        """
        self.__record_size = record_size        # истинный размер записи, который не использует байт состояния
        mode = "w+b" if not os.path.exists(filename) else "r+b" # предотвращение усечения файла при открытии
        self.__fh = open(filename, mode)
        self.auto_flush = auto_flush            # выталкивание файла на диск
    @property
    def record_size(self):
        """Размер каждого элемента"""
        return self.__record_size

    @property
    def name(self):
        """Имя файла"""
        return self.__fh.name

    def flush(self):
        """Выталкивание файла на диск
        Совершается автоматически, если auto_flush равен True
        """
        self.__fh.flush()

    def close(self):
        self.__fh.close()

    def append(self, record):
        """Функция реализующая метод перемещающий указатель в конец файла
        и производящий вывод записи в файл."""
        assert isinstance(record, (bytes, bytearray)), \
            "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
                self.record_size))
        self.__fh.seek(0, os.SEEK_END)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()

    def __setitem__(self, index, record):
        """Устанавливает элемент с индексом позиции как заданную запись

        Позиция индекса может быть за пределами текущего конца файла.
        """
        assert isinstance(record, (bytes, bytearray)), \
            "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
                self.record_size))
        self.__seek_to_index(index)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()

    def __getitem__(self, index):
        """Возвращает элемент в указанной позиции индекса

        Если в данной позиции нет элемента, возникает исключение IndexError.
        Если элемент в данной позиции был удален, возвращается None.
        """
        self.__seek_to_index(index)
        return self.__fh.read(self.record_size)

    def __seek_to_index(self, index):
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        offset = index * self.record_size
        if offset >= end:
            raise IndexError("no record at index position {0}".format(
                index))
        self.__fh.seek(offset)

    def __delitem__(self, index):
        """Удаляет элемент в указанной позиции индекса
        и перемещает следующие записи вверх.
        """
        length = len(self)
        for following in range(index + 1, length):
            self[index] = self[following]
            index += 1
        self.__fh.truncate((length - 1) * self.record_size)
        self.__fh.flush()

    def __len__(self):
        """Количество количества записей."""
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        return end // self.record_size


if __name__ == "__main__":
    import shutil
    import sys

    S = struct.Struct("<15s")
    fileA = os.path.join(tempfile.gettempdir(), "fileA.dat")
    fileB = os.path.join(tempfile.gettempdir(), "fileB.dat")
    for name in (fileA, fileB):
        try:
            os.remove(name)
        except EnvironmentError:
            pass

    brf = BinaryRecordFile(fileA, S.size)
    for text in ("Alpha", "Bravo", "Charlie", "Delta",
                 "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
                 "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
                 "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor",
                 "Whisky", "X-Ray", "Yankee", "Zulu"):
        brf.append(S.pack(text.encode("utf8")))
    assert len(brf) == 26
    brf.append(S.pack(b"Extra at the end"))
    assert len(brf) == 27
    shutil.copy(fileA, fileB)
    del brf[12]
    del brf[0]
    del brf[24]
    assert len(brf) == 24, len(brf)
    brf.close()

    if (os.path.getsize(fileA) + (3 * S.size)) != os.path.getsize(fileB):
        print("FAIL#1: expected file sizes are wrong")
        sys.exit()

    shutil.copy(fileB, fileA)
    if os.path.getsize(fileA) != os.path.getsize(fileB):
        print("FAIL#2: expected file sizes differ")
        sys.exit()

    for name in (fileA, fileB):
        try:
            os.remove(name)
        except EnvironmentError:
            pass
