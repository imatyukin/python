#!/usr/bin/env python3
import codecs
import re

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
for n in l2circuit_ifl:
    n = n.split('.')[0] + ' unit ' + n.split('.')[1]
    l2circuit_ifl_unit.append(n)
print(l2circuit_ifl_unit)

# выводим конфигурацию интерфейсов l2circuit для специфичесого ifd
for line in srouter_setline:
    for unit in l2circuit_ifl_unit:
        unit = re.compile(r'\b(?:%s)\b' % '|'.join(l2circuit_ifl_unit))
        print(unit)
