#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from decimal import Decimal
from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt
import re

DATE=re.compile(r'^(\d\d\d\d)-(\d\d)-(\d\d)$')
def date_from_str(x):
    M = DATE.search(x)
    if not M:
        raise ValueError(f'Invalid date {x}')
    y, m, d = map(int, M.groups())
    return date(y,m,d)


def read_data(file):
    rdr = csv.reader(file)
    for x in rdr:
        dt, scale, price = x
        scale = int(scale)
        price = Decimal(price)
        dt = date.fromisoformat(dt)
        yield (dt, scale, price)


def show_data(seq):
    data = list(seq)
    dates  = np.array([ dt for dt, *_ in data ])
    prices = np.array([ x[2] for x in data ])
    plt.plot(dates, prices)
    plt.show()


def show(filename):
    with open(filename, 'rt', encoding='utf-8') as src:
        seq = read_data(src)
        show_data(seq)


if __name__ == '__main__':
    show('course.csv')

