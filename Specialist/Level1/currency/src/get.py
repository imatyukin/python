#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from get_data import courses

url  = 'http://cbr.ru/currency_base/dynamics/'
url += '?UniDbQuery.Posted=True'
url += '&UniDbQuery.mode=1'
url += '&UniDbQuery.date_req1='
url += '&UniDbQuery.date_req2='
url += '&UniDbQuery.VAL_NM_RQ=R01235'
url += '&UniDbQuery.FromDate=01.01.2018'
url += '&UniDbQuery.ToDate=29.11.2018'

def get(filename):
    with open(filename, 'wt',
              encoding='utf-8', newline='') as trg:
        wrt = csv.writer(trg)
        seq = courses(url, encoding='utf-8')
        for iks in seq:
            wrt.writerow(iks)


if __name__ == '__main__':
    get('course.csv')






