#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from decimal import Decimal
from datetime import date
import numpy as np
import matplotlib.pyplot as plt


def read_data(file):
    rdr = csv.reader(file)
    for x in rdr:
        dt, scale, price = x
        scale = int(scale)
        price = Decimal(price)
        dt = date.fromisoformat(dt)
        yield(dt, scale, price)


def show_data(seq):
    data = list(seq)
    dates = np.array([ dt for dt, *_ in data ])
    prices = np.array([ pr for *_, pr in data ])
    plt.plot(dates, prices)
    plt.show()


def show(filename):
    with open(filename, 'rt', encoding='utf-8') as src:
        seq = read_data(src)
        show_data(seq)
        

if __name__ == '__main__':
    show('course.csv')