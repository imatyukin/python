#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import get_data

print('Лучшие 5 результатов')

counter = 0
result_dict = {}
worst_result = 0

while counter < 5:
    participant = get_data.next_person()
    result = get_data.next_result()
    
    result_dict[participant] = result

    if worst_result < result:
        worst_result = result

    for k, v in result_dict.items():
        print(k, v)
    print()
    
    counter += 1

while True:
    participant = get_data.next_person()
    result = get_data.next_result()
    
    if result < worst_result:
        for k, v in result_dict.items():
            if v == worst_result:
                result_dict.pop(k)
                break
        worst_result = sorted(result_dict.values())[-1]
        result_dict[participant] = result
    
    for k, v in result_dict.items():
        print(k, v)
    print()

    if result > worst_result:
        for k, v in result_dict.items():
            print(k, v)
        continue
