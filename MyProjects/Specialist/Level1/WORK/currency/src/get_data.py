#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
from datetime import date
from decimal import Decimal

def get_lines(url, *, encoding=None):
    with urlopen(url) as src:
        data = b''
        while True:
            while b'\n' in data:
                n = data.index(b'\n')+1
                result = data[:n]
                data = data[n:]
                if encoding is not None:
                    result = result.decode(encoding)
                yield result
            chunk = src.read(1024)
            if not chunk:
                break
            data += chunk
    if data:
        if encoding is not None:
            data = data.decode(encoding)
        yield data


DATE = re.compile(r'''
    ^<td>
    (\d?\d) # день
    \.
    (\d\d) # месяц
    \.
    (\d\d\d\d) # год
    </td>$
    ''', re.VERBOSE)

SCALE = re.compile(r'^<td>(\d+)</td>$')

PRICE = re.compile(r'''
    ^<td>
    (\d+) # рубли
    [,\.]
    (\d\d\d\d) # сотые доли копейки
    </td>$
    ''', re.VERBOSE)



def clean_lines(seq):
    seq = map(str.strip, seq)
    seq = filter(lambda x: x, seq)
    for x in seq:
        M = DATE.search(x)
        if M:
            day, month, year = map(int, M.groups())
            yield date(year, month, day)
            continue
        M = SCALE.search(x)
        if M:
            yield int(M.group(1))
            continue
        M = PRICE.search(x)
        if M:
            rub, kop = M.groups()
            yield Decimal(f'{rub}.{kop}')


def collect_data(seq):
    seq = iter(seq)
    try:
        while True:
            dt = next(seq)
            if not isinstance(dt, date):
                raise TypeError('Invalid type of date')
            scale = next(seq)
            if not isinstance(scale, int):
                raise TypeError('Invalid type of scale')
            price = next(seq)
            if not isinstance(price, Decimal):
                raise TypeError('Invalid type of price')
            yield ( dt, scale, price )
    except StopIteration:
        pass


def courses(url, *, encoding):
    seq = get_lines(url, encoding=encoding)
    seq = clean_lines(seq)
    seq = collect_data(seq)
    return seq
