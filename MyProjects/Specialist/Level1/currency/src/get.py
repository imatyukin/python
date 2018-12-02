#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from get_data import courses

url = 'http://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.FromDate=01.01.2018&UniDbQuery.ToDate=29.11.2018'


def get(filename):
    with open(filename, 'wt', encoding='utf-8', newline='') as trg:
        wrt = csv.writer(trg) 
        seq = courses(url, encoding='utf-8')
        for x in seq:
            wrt.writerow(x)


if __name__ == '__main__':
    get('course.csv')