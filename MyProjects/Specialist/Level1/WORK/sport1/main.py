#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import get_data
import out_data

all_people = []

for r in get_data.coming():

    all_people.append(r)
    all_people.sort()
    if len(all_people) > 5:
        del all_people[-1]
    out_data.out_all(all_people)
else:
    print('ОПАНЬКИ')

