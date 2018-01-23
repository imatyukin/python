#!/usr/bin/env python3
import codecs
import re

# show | display set | save /var/tmp/spbr-ar1.conf
srouter = codecs.open('spbr-ar1.conf', 'r', encoding='utf-8', errors='ignore').read()
# show | display set | save /var/tmp/spbr-ar4.conf
trouter = codecs.open('spbr-ar4.conf', 'r', encoding='utf-8', errors='ignore').read()

ifl_regex=re.compile("xe-10/1/0.*")
ifd_regex=re.compile("xe-10/1/0")
# специфический ifl
ifl_spec_regex=re.compile("xe-10/1/0.+14750")

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

# вывод настроек специфического ifl
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'set interfaces' in setline:
            print(setline)

# вывод настроек cos специфического ifl
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'set class-of-service' in setline:
            print(setline)

# вывод настроек vrf l2vpn специфического ifl
for setline in srouter_setline:
    for i in re.findall(ifl_spec_regex, setline):
        if 'set protocols l2circuit' in setline:
            print(setline)
            break

# вывод настроек vrf l3vpn специфического ifl (активировать при l3vpn)
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
