#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def out_all(people : list) -> None :
    max_len = 0
    for _, fam in people:
        if len(fam) > max_len:
            max_len = len(fam)
    print('-'*40)
    print('{0:{2}} {1:7}'.format('Фамилия', 'Результат', max_len))
    print('- '*20)
    for res, fam in people:
        text = f'{fam:{max_len}} -- {res:7.2f}'
        print(text)
    print('-'*40)
