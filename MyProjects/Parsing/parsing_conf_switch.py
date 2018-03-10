#!/usr/bin/env python3
# Поиск VLANов коммутатора на терминирующем маршрутизаторе
import sys
import codecs


class Tee(object):
    # Output on the console and file

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


# Конфигуационные файлы коммутатора и маршрутизатора
# show | display set | save /var/tmp/switch.conf
switch_conf = 'spbr-astk1.conf'
router_conf = 'spbr-ar2.conf'
# Файл вывода результатов
f_out = 'a.out'
# Интерфейс коммутатора
switch_ifd = ' ge-0/0/1 '
# Интерфейсы маршрутизатора
router_ifd = ' xe-9/3/3 '


def main():
    # Объявление глобальных переменных
    global switch_conf, router_conf, f_out
    global switch_ifd, router_ifd

    with open(f_out, 'w') as f_out:
        # This will go to stdout and the file
        original = sys.stdout
        sys.stdout = Tee(sys.stdout, f_out)

        switch_conf = codecs.open(switch_conf, 'r', encoding='utf-8', errors='ignore').read()
        switch_conf = switch_conf.splitlines()
        router_conf = codecs.open(router_conf, 'r', encoding='utf-8', errors='ignore').read()
        router_conf = router_conf.splitlines()

        # Находим все VLANы на физ. интерфейсе (ifd) коммутатора
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

        # Находим все VLANы на физ. интерфейсах (ifd) маршрутизатора
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

        # Находим общие значения двух словарей (VLANы)
        for sw_ifd, sw_vlan in sw_vlans.items():
            for r_ifd, r_vlan in r_vlans.items():
                for i in sw_vlan:
                    for j in r_vlan:
                        if i == j:
                            print(r_ifd, r_vlan)


        sys.stdout = original
        # Only on stdout


if __name__ == "__main__":
    main()