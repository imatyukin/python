#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from decimal import Decimal
from flight import Flight


def all_flights(filepath):
    with open(filepath, 'rt', encoding='utf-8') as src:
        rdr = csv.reader(src)
        for start, finish, start_time, finish_time in rdr:
            h, m = start_time.split(':')
            start_time = int(h) + int(m)/60
            h, m = finish_time.split(':')
            finish_time = int(h) + int(m)/60
            yield Flight( start, finish, start_time, finish_time )


def collect_flights(filepath):
    result = {}
    for f in all_flights(filepath):
        try:
            result[f.start].append(f)
        except KeyError:
            result[f.start] = [ f ]
    return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    