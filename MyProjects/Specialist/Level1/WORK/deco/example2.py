#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from datetime import datetime


@contextmanager
def profile():
    start = datetime.now()
    try:
        yield None
    finally:
        t = datetime.now()-start
        print('>>>>', t, '<<<<')

with profile():
    for k in range(0,100000):
        print(k)
