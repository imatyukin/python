#!/usr/bin/env python3
import sys
import codecs
import re

sys.stdout = open('spbr-ar4', 'w')

# show | display set | save /var/tmp/spbr-ar1.conf
srouter = codecs.open('spbr-ar1.conf', 'r', encoding='utf-8', errors='ignore').read()
# show | display set | save /var/tmp/spbr-ar4.conf
trouter = codecs.open('spbr-ar4.conf', 'r', encoding='utf-8', errors='ignore').read()

# все логические ifl на ifd
ifl_regex=re.compile("xe-10/1/0.*")
# специфический ifd
ifd_regex=re.compile("xe-10/1/0")
# специфический ifl
ifl_unit_regex=re.compile("xe-10/1/0 unit 14844")
ifl_spec_regex=re.compile("xe-10/1/0\.14844")


# поиск всех ifd и ifl
srouter_setline = srouter.splitlines()
srouter_ifd = []
srouter_ifl = []
for setline in srouter_setline:
    if 'set interfaces' in setline:
        for fields in setline.splitlines():
            srouter_ifd.append(fields.split()[2])
            if 'unit' in fields.split()[3]:
                srouter_ifl.append(fields.split()[2] + '.' + fields.split()[4])
used = set()
srouter_ifd = [x for x in srouter_ifd if x not in used and (used.add(x) or True)]
srouter_ifl = [x for x in srouter_ifl if x not in used and (used.add(x) or True)]
# print(srouter_ifd)
# print(srouter_ifl)

# поиск всех ifl на специфическом ifd
ifl = ([m.group(0) for l in srouter_ifl for m in [ifl_regex.search(l)] if m])
# print(ifl)

'''
# вывод настроек специфического ifl
print("---------- Настройки интерфейса ----------")
for setline in srouter_setline:
    for i in re.findall(ifl_unit_regex, setline):
        if 'set interfaces' in setline:
            print(setline)

# вывод настроек cos специфического ifl
print("---------- Настройки CoS ----------")
for setline in srouter_setline:
    for i in re.findall(ifl_unit_regex, setline):
        if 'set class-of-service' in setline:
            print(setline)

# вывод настроек vrf l2vpn специфического ifl
print("---------- Настройки L2VPN ----------")
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'set protocols l2circuit' in setline:
            print(setline)

# вывод настроек vrf l3vpn специфического ifl
print("---------- Настройки L3VPN ----------")
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'routing-instances' in setline:
            vrf_name = [fields.split()[2] for fields in setline.splitlines()]
for setline in srouter_setline:
        try:
            if str(vrf_name)[2:-2] in setline:
                print(setline)
        except:
            pass

# вывод остальных настроек специфического ifl
print("---------- Остальные настройки ----------")
for setline in srouter_setline:
    for i in re.findall(ifl_unit_regex, setline):
        if 'set interfaces' not in setline:
            if 'set class-of-service' not in setline:
                if 'set protocols l2circuit' not in setline:
                    if 'routing-instances' not in setline:
                        print(setline)
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'set interfaces' not in setline:
            if 'set class-of-service' not in setline:
                if 'set protocols l2circuit' not in setline:
                    if 'routing-instances' not in setline:
                        print(setline)
'''

# перенос l2vpn с одного интерфейса маршрутизатора на другой маршрутизатор

# узнаём все интерфейсы связанные с l2vpn на специфическом ifd
l2circuit_ifl = []
local_switch_ifl = []
for line in srouter_setline:
    for l2vpn_ifl in re.findall(ifd_regex, line):
        if 'set protocols l2circuit' in line:
            if 'set protocols l2circuit neighbor' in line:
                l2circuit_ifl.extend(([fields.split()[6] for fields in line.splitlines()]))
            if 'set protocols l2circuit local-switching' in line:
                local_switch_ifl.extend(([fields.split()[5] for fields in line.splitlines()]))
                if 'end-interface interface' in line:
                    local_switch_ifl.extend(([fields.split()[8] for fields in line.splitlines()]))
used = set()
l2circuit_ifl = [x for x in l2circuit_ifl if x not in used and (used.add(x) or True)]
used = set()
local_switch_ifl = [x for x in local_switch_ifl if x not in used and (used.add(x) or True)]
# local-switching ifl для специфического ifd
local_switch_ifl_ifd = list(filter(ifl_regex.search, local_switch_ifl))
# ifl с которыми настроен local-switching специфического ifd
local_switch_ifl_filtered = list(filter(lambda i: not ifl_regex.search(i), local_switch_ifl))
# print(l2circuit_ifl)
# print(local_switch_ifl_ifd)
# print(local_switch_ifl_filtered)

# разделяем ifl на ifd и unit
l2circuit_ifl_unit = []
replace_l2circuit_ifd_unit = []
for n in l2circuit_ifl:
    n = ' ' + n.split('.')[0] + ' unit ' + n.split('.')[1] + ' '
    l2circuit_ifl_unit.append(n)
# print(l2circuit_ifl_unit)
local_switch_ifl_ifd_unit = []
replace_local_switch_ifl_ifd_unit = []
for n in local_switch_ifl_ifd:
    n = ' ' + n.split('.')[0] + ' unit ' + n.split('.')[1] + ' '
    local_switch_ifl_ifd_unit.append(n)
# print(local_switch_ifl_ifd_unit)

# выводим конфигурацию интерфейсов l2circuit для специфичесого ifd с заменой его имени
for line in srouter_setline:
    for unit in l2circuit_ifl_unit:
        if unit in line:
            print(line.replace(unit.split( )[0], 'xe-0/1/2'))
for line in srouter_setline:
    for unit in l2circuit_ifl:
        unit = ' ' + unit + ' '
        if unit in line:
            print(line.replace(unit.split('.')[0], ' xe-0/1/2'))

# выводим конфигурацию интерфейсов local-switching для специфичесого ifd с заменой его имени
for line in srouter_setline:
    for unit in local_switch_ifl_ifd_unit:
        if unit not in (' xe-10/1/0 unit 4700 ', ' xe-10/1/0 unit 4800 ', ' xe-10/1/0 unit 4900 ', ' xe-10/1/0 unit 11000 '):
            if unit in line:
                print(line.replace(unit.split( )[0], 'xe-0/1/2'))

# если local-switching на одном и том же ifd
local_switch_list = []
for line in srouter_setline:
    for unit in local_switch_ifl_ifd:
        if 'neighbor 95.167.88.60' not in line:
            unit = ' ' + unit
            if line.endswith(unit):
                local_switch_list.append(line)
for item in local_switch_list:
    if 'set protocols l2circuit local-switching interface xe-10/1/0' in item:
        print(item.replace('xe-10/1/0', 'xe-0/1/2'))

# если local-switching на разных ifd
local_switch_unit_start = []
for line in srouter_setline:
    for unit in local_switch_ifl_ifd:
        if unit not in (' xe-10/1/0.4700 ', ' xe-10/1/0.4800 ', ' xe-10/1/0.4900 ', ' xe-10/1/0.11000 ', ' xe-10/1/0.14700 '):
            unit = ' ' + unit + ' '
            if unit in line:
                if 'set protocols l2circuit local-switching interface xe-10/1/0' in line:
                    if 'end-interface interface xe-10/1/0' not in line:
                        local_switch_unit_start.append(unit)
                        if 'description' in line:
                            print(line.replace('set protocols l2circuit local-switching interface xe-10/1/0', 'set protocols l2circuit neighbor 87.226.134.133 interface xe-0/1/2'))

used = set()
local_switch_unit_start = [x for x in local_switch_unit_start if x not in used and (used.add(x) or True)]
for unit in local_switch_unit_start:
    if unit not in (' xe-10/1/0.4700 ', ' xe-10/1/0.4800 ', ' xe-10/1/0.4900 ', ' xe-10/1/0.11000 '):
        print('set protocols l2circuit neighbor 87.226.134.133 interface xe-0/1/2' + '.' + unit.split('.')[1] + 'ignore-mtu-mismatch')
        print('set protocols l2circuit neighbor 87.226.134.133 interface xe-0/1/2' + '.' + unit.split('.')[1] + 'virtual-circuit-id ' + unit.split('.')[1])

# если ifd end-interface в local-switching
local_switch_unit_end = []
for line in srouter_setline:
    for unit in local_switch_ifl_ifd:
        if unit not in (' xe-10/1/0.4700 ', ' xe-10/1/0.4800 ', ' xe-10/1/0.4900 ', ' xe-10/1/0.11000 '):
            unit = ' ' + unit
            if unit in line:
                if 'end-interface interface' + unit in line:
                    print('set protocols l2circuit neighbor 87.226.134.133 interface xe-0/1/2' + '.' + unit.split('.')[1] + ' ignore-mtu-mismatch')
                    print('set protocols l2circuit neighbor 87.226.134.133 interface xe-0/1/2' + '.' + unit.split('.')[1] + ' virtual-circuit-id ' + unit.split('.')[1])

sys.stdout.close()

sys.stdout = open('spbr-ar1', 'w')

make_l2circuit_start_dict = {}
for line in srouter_setline:
    for unit in local_switch_ifl:
        if not line.startswith('set protocols l2circuit local-switching interface xe-10/1/0.'):
            if 'end-interface interface xe-10/1/0' in line:
                unit = ' ' + unit + ' '
                if unit in line:
                    match = re.search(ifl_regex, line).group(0)
                    make_l2circuit_start_dict.update({unit : match})
                    if 'description' in line:
                        print(line.replace('set protocols l2circuit local-switching interface', 'set protocols l2circuit neighbor 213.59.207.99 interface'))
make_l2circuit_end_dict = {}
for line in srouter_setline:
    for unit in local_switch_ifl:
        unit = ' ' + unit
        if line.startswith('set protocols l2circuit local-switching interface xe-10/1/0.'):
            if 'end-interface interface xe-10/1/0' not in line:
                if 'end-interface interface' + unit in line:
                    match = re.search('xe-10/1/0.\w+', line).group(0)
                    make_l2circuit_end_dict.update({unit: match})

for k, v in make_l2circuit_start_dict.items():
    print('set protocols l2circuit neighbor 213.59.207.99 interface' + k + 'virtual-circuit-id ' + v.split('.')[1])
    print('set protocols l2circuit neighbor 213.59.207.99 interface' + k + 'ignore-mtu-mismatch')
    print('deactivate protocols l2circuit neighbor 213.59.207.99 interface' + k)
for k, v in make_l2circuit_end_dict.items():
    print('set protocols l2circuit neighbor 213.59.207.99 interface' + k + ' virtual-circuit-id ' + v.split('.')[1])
    print('set protocols l2circuit neighbor 213.59.207.99 interface' + k + ' ignore-mtu-mismatch')
    print('deactivate protocols l2circuit neighbor 213.59.207.99 interface' + k)

sys.stdout.close()