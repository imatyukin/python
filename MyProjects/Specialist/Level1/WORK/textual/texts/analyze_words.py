#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def analyze_words(word_seq):
    result = {}
    for w in word_seq:
        try:
            result[w] += 1
        except KeyError:
            result[w] = 1
    return result
