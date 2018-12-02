#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import texts

with open('voyna-i-mir-tom-1.txt',
          'rt', encoding='windows-1251') as src:
    ws = texts.words_from_file(src)
    word_data = texts.analyze_words(ws)

with open('letters.txt',
          'wt', encoding='utf-8',
          newline='') as trg:
    texts.out_by_letters(word_data, file=trg)

with open('freq.txt',
          'wt', encoding='utf-8',
          newline='') as trg:
    texts.out_by_freq(word_data, file=trg)