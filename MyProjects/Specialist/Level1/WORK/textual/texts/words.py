#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def words_from_file(source):
    for line in source:
        wrd = line.split()
        for x in wrd:
            yield x
