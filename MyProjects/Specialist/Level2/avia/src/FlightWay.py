#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import suppress
from collections.abc import Sequence

class InvalidFlight(ValueError): pass


class FlightWay(Sequence):

    def __init__(self, *flights):
        self.__flights = []
        for x in flights:
            self.append(x)
        
    def __getitem__(self, index):
        return self.__flights[index]
        
    def __len__(self):
        return len(self.__flights)
        
    def append(self, new_flight):
        with suppress(IndexError):
            if self.__flights[-1].finish != new_flight.start:
                raise InvalidFlight('Invalid Flight')
        self.__flights.append(new_flight)

    def __add__(self, other):
        result = FlightWay()
        result.__flights = list(self.__flights)
        for x in other:
            result.append(x)
        return result
    
    def __radd__(self, other):
        result = FlightWay()
        result = result.__add__(other)
        result = result.__add__(self)
        return result
    
    def __contains__(self, item):
        if super().__contains__(item):
            return True
        for f in self.__flights:
            if item == f.start or item == f.finish:
                return True
        return False
    
    def __str__(self):
        return str(self.__flights)
        
    __repr__ = __str__
    
    def wait_time(self, index):
        f = self[index].finish_time
        s = self[index+1].start_time
        result = s - f
        if result < 0.0:
            result += 24.0
        return result
    
    @property
    def duration(self):
        result = sum(( x.duration for x in self ))
        #result += sum(( self.wait_time(k) for k in range(0,len(self)-1)))
        for k in range(0,len(self)-1):
            result += self.wait_time(k)
        return result
