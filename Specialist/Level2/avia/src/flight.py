#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Flight(object):

    def __init__(self, start, finish, start_time, finish_time):
        self.__start = start
        self.__finish = finish
        self.__start_time = start_time
        self.__finish_time = finish_time
        
    @property
    def start(self):
        return self.__start

    @property
    def finish(self):
        return self.__finish

    @property
    def start_time(self):
        return self.__start_time

    @property
    def finish_time(self):
        return self.__finish_time

    @property
    def duration(self):
        result = self.finish_time - self.start_time
        if result < 0:
            result += 24
        return result

    def __str__(self):
        s = f'{self.start} ({self.start_time:.3f})'
        f = f'{self.finish} ({self.finish_time:.3f})'
        return f'{s} -> {f} -- {self.duration:.3f}'

    __repr__ = __str__
