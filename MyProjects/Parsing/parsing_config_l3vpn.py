#!/usr/bin/env python3
import re
import operator

#  вывод команды: SPBR-AR1> show configuration | match xe-10/1/0 | match routing-instance | display set
ifl_ri = open('ifl_ri', 'r').read()

# поиск интерфейсов входящих в vrf
ifl = [fields.split()[4] for fields in ifl_ri.splitlines()]
regex=re.compile("xe-10/1/0.*")
list_ifl = ([m.group(0) for l in ifl for m in [regex.search(l)] if m])
print(list_ifl)

# поиск названий routing-instance с найденными интерфейсами
ifl_ri = ifl_ri.splitlines()
list_ri = []
for item in list_ifl:
    for line in ifl_ri:
        if item in line:
            list_ri.extend(([fields.split()[2] for fields in line.splitlines()]))
# print(list_ri)

# вывод команды: SPBR-AR1> show configuration routing-instances | display set
source_ri = open('source_ri', 'r').read()

# поиск названий routing-instance с instance-type vrf
source_ri_line = source_ri.splitlines()
list_vrf = []
for ri in list_ri:
    for line in source_ri_line:
        if 'instance-type vrf' in line:
            if ri in line:
                list_vrf.extend(([fields.split()[2] for fields in line.splitlines()]))
# print(list_vrf)

# поиск номеров vrf
dict_vrf_num = {}
for line in source_ri_line:
    if 'route-distinguisher' in line:
        name = [fields.split()[2] for fields in line.splitlines()]
        rd = [fields.split()[4] for fields in line.splitlines()]
        # rd = [(fields.split()[4]).split(":")[1] for fields in line.splitlines()]
        dict_vrf_num.update(dict(zip(name, rd)))
# print(dict_vrf_num)

# сравнение списка list_vrf с ключом словаря dict_vrf_num (поиск номеров только для l3vpn)
dict_vrf = {k: dict_vrf_num[k] for k in dict_vrf_num.keys() & set(list_vrf)}
# print(dict_vrf)

# сортировка словаря
sorted_dict_vrf = sorted(dict_vrf.items(), key=operator.itemgetter(1))
# sorted_dict_vrf = sorted(dict_vrf.items(), key=lambda x: int(x[1]))
print(sorted_dict_vrf)

# вывод команды: SPBR-AR2> show configuration routing-instances | display set
target_ri = open('target_ri', 'r').read()

# поиск названий routing-instance с instance-type vrf
target_ri_line = target_ri.splitlines()
list_target_vrf = []
for target_ri in target_ri_line:
    if 'instance-type vrf' in target_ri:
        list_target_vrf.extend(([fields.split()[2] for fields in target_ri.splitlines()]))
# print(list_target_vrf)

# поиск номеров vrf
dict_target_vrf_num = {}
for target_line in target_ri_line:
    if 'route-distinguisher' in target_line:
        target_name = [fields.split()[2] for fields in target_line.splitlines()]
        target_rd = [fields.split()[4] for fields in target_line.splitlines()]
        # target_rd = [(fields.split()[4]).split(":")[1] for fields in target_line.splitlines()]
        dict_target_vrf_num.update(dict(zip(target_name, target_rd)))
# print(dict_target_vrf_num)

# сравнение списка list_target_vrf с ключом словаря dict_target_vrf_num (поиск номеров только для l3vpn)
dict_target_vrf = {k: dict_target_vrf_num[k] for k in dict_target_vrf_num.keys() & set(list_target_vrf)}
# print(dict_target_vrf)

# сортировка словаря
sorted_dict_target_vrf = sorted(dict_target_vrf.items(), key=operator.itemgetter(1))
# sorted_dict_target_vrf = sorted(dict_target_vrf.items(), key=lambda x: int(x[1]))
print(sorted_dict_target_vrf)
