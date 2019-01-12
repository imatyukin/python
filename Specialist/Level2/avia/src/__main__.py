#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from all_flights import collect_flights
from os.path import join, abspath
import pprint
import search

data_path = join('data', 'data.csv') # обязательно
data_path = abspath(data_path) # не обязательно, но рекомендуется

flights = collect_flights(data_path)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(flights)

print('-'*40)

for way in search.by_width(flights, 'Москва', 'Магадан'):
    print(way.duration)
    pp.pprint(way)
