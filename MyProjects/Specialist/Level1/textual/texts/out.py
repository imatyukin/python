#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv


def out_by_letters(words, file):
    data = list(words.items())
    data.sort()
    wrt = csv.writer(file)
    for x in data:
        wrt.writerow(x)


def out_by_freq(words, file):
    data = [ (f,w) for w, f in words.items() ]
    data.sort(reverse=True)
    wrt = csv.writer(file)
    for x in data:
        wrt.writerow(x)