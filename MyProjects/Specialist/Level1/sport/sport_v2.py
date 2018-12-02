#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import get_data_v2
import out_data

all_sportsmens = []

for r in get_data_v2.coming():
    all_sportsmens.append(r)
    all_sportsmens.sort()
    if len(all_sportsmens) > 5:
        del all_sportsmens[-1]
    out_data.out_all(all_sportsmens)
else:
    print('Опаньки')
