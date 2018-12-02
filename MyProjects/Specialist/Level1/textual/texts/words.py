#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def words_from_file(source):
    for line in source:
        yield from line.split(' ')
