#!/usr/bin/env python3
''' Перенос L2VPN с SPBR-AR1@xe-9/1/0 на SPBR-AR2@xe-4/1/2 '''
import codecs
import re

# show | display set | save /var/tmp/spbr-ar1.conf
router_conf = codecs.open('spbr-ar1.conf', 'r', encoding='utf-8', errors='ignore').read()
router_conf_line = router_conf.splitlines()

# Регулярные выражения
ifl_regex = re.compile('xe-9/1/0.\w+')
ifd_source = 'xe-9/1/0'
ifd_target = 'xe-4/1/2'
ifl_except = ' xe-9/1/0 unit 4700 ', ' xe-9/1/0 unit 4800 ', ' xe-9/1/0 unit 4900 ', ' xe-9/1/0 unit 11000 ', ' xe-9/1/0 unit 14700 '

# Логические интерфейсы L2VPN (ifl) связанные с физическим интерфейсом ifd
neighbor_ifl = []
local_switching_ifl = []
for conf_line in router_conf_line:
    if 'set protocols l2circuit' in conf_line:
        if 'set protocols l2circuit neighbor' in conf_line:
            if re.findall(ifl_regex, conf_line):
                neighbor_ifl.extend(([fields.split()[6] for fields in conf_line.splitlines()]))
        if 'set protocols l2circuit local-switching' in conf_line:
            if 'end-interface' in conf_line:
                if re.findall(ifl_regex, conf_line):
                    for fields in conf_line.splitlines():
                        local_switching_ifl.append(fields.split()[5])
                        local_switching_ifl.append(fields.split()[8])
# Уникальные значения ifl для l2circuit neighbor
used = set()
neighbor_ifl = [x for x in neighbor_ifl if x not in used and (used.add(x) or True)]
# print(neighbor_ifl)
# local-switching ifl связанные с ifd
local_switching_ifl_ifd = list(filter(ifl_regex.search, local_switching_ifl))
# print(local_switching_ifl_ifd)
# ifl других ifd с которыми настроен local-switching
local_switching_ifl_filtered = list(filter(lambda i: not ifl_regex.search(i), local_switching_ifl))
# print(local_switching_ifl_filtered)

# разделяем ifl на ifd и unit
neighbor_ifd_unit = []
for ifl in neighbor_ifl:
    ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
    neighbor_ifd_unit.append(ifl)
# print(neighbor_ifd_unit)
local_switching_ifd_unit = []
for ifl in local_switching_ifl_ifd:
    ifl = ' ' + ifl.split('.')[0] + ' unit ' + ifl.split('.')[1] + ' '
    local_switching_ifd_unit.append(ifl)
# print(local_switching_ifd_unit)

# выводим конфигурацию l2circuit neighbor для ifd с заменой его имени на новое
for conf_line in router_conf_line:
    for unit in neighbor_ifd_unit:
        if unit in conf_line:
           print(conf_line.replace(unit.split( )[0], ifd_target))
for conf_line in router_conf_line:
    for unit in neighbor_ifl:
        unit = ' ' + unit + ' '
        if unit in conf_line:
            print(conf_line.replace(unit.split('.')[0], ' ' + ifd_target))
# выводим конфигурацию l2circuit local-switching для ifd с заменой его имени на новое
for conf_line in router_conf_line:
    for unit in local_switching_ifd_unit:
        if unit not in ifl_except:
            if unit in conf_line:
                print(conf_line.replace(unit.split( )[0], ifd_target))
# если local-switching на одном ifd заменяем его имя на новое
local_switching_list = []
for conf_line in router_conf_line:
    for unit in local_switching_ifl_ifd:
        unit = ' ' + unit
        if conf_line.endswith(unit):
            local_switching_list.append(conf_line)
            print(local_switching_list)
for i in local_switching_list:
    if 'set protocols l2circuit local-switching interface ' + ifd_source in i:
        print(i.replace(ifd_source, ifd_target))