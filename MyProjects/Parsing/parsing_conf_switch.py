#!/usr/bin/env python3
import sys
import codecs


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


switch_conf = 'spbr-astk1.conf'
router_conf = 'spbr-ar2.conf'
target_conf = 'target.conf'
switch_ifd = ' ge-0/0/1 '
router_ifd = ' xe-9/3/3 '


def main():
    global switch_conf, router_conf, target_conf
    global switch_ifd, router_ifd

    with open(target_conf, 'w') as target_conf:
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, target_conf)

        switch_conf = codecs.open(switch_conf, 'r', encoding='utf-8', errors='ignore').read()
        switch_conf = switch_conf.splitlines()
        router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read()
        router_conf = router_conf.splitlines()

        # Находим все VLANs на физ. интерфейсе (ifd) коммутатора
        # Создаём словарь sw_vlans {ifd: [VLANs]}
        sw_vlans = {}
        for line in switch_conf:
            if switch_ifd in line:
                if 'vlan members' in line:
                    line = str(line).split(' ')
                    key = line[2].strip()
                    value = line[9].strip()
                    if '-' in value:
                        value = str(value).split('-')
                        value = list(range(int(value[0]), int(value[1])+1))
                    else:
                        value = int(value.split()[-1])
                    if key not in sw_vlans:
                        sw_vlans.setdefault(key, []).append(value)
                    else:
                        if isinstance(value, list):
                            for v in value:
                                sw_vlans[key].append(v)
                        else:
                            sw_vlans[key].append(value)
        # print(sw_vlans)

        # Находим все VLANs на физ. интерфейсе (ifd) маршрутизатора
        # Создаём словарь r_vlans {ifd.unit: [vlan]}
        r_vlans = {}
        for line in router_conf:
            if 'set interfaces' + router_ifd in line:
                if 'unit' in line:
                    if ' vlan-id ' in line:
                        if 'input-vlan-map' not in line:
                            line = str(line).split(' ')
                            key = line[2].strip() + '.' + line[4].strip()
                            value = line[6].strip()
                            value = int(value.split()[-1])
                            if key not in r_vlans:
                                r_vlans.setdefault(key, []).append(value)
                            else:
                                r_vlans.key = value
        # print(r_vlans)

        # Сравниваем значения двух словарей
        for sw_k, sw_v in sw_vlans.items():
            for r_k, r_v in r_vlans.items():
                for i in sw_v:
                    for j in r_v:
                        if i == j:
                            print(r_k, r_v)


        sys.stdout = original


if __name__ == "__main__":
    main()