#!/usr/bin/env python3
# Поиск VLANов коммутатора на терминирующем маршрутизаторе
import sys
import codecs
import re


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
# show | display set | save /var/tmp/router.conf
router_conf = 'spbr-ar2.conf'

# Файл вывода результатов
f_out = 'a.out'

# Интерфейсы коммутатора
# в сторону маршрутизатора
switch_ifd = ' ge-0/0/1 '
# в сторону коммутаторов связанных с маршрутизатором
switch_to_sw_ifd = [' ge-0/0/14 ', ' ge-0/0/21 ']

# Интерфейсы маршрутизатора
# регулярное выражение для всех лог. интерфейсов (ifl) в сторону коммутатора
router_ifl_regex = re.compile('xe-9/3/3.\w+')
# в сторону всех коммутаторов
router_ifd = [' xe-0/0/2 ', ' xe-4/1/2 ', ' xe-5/3/0 ', ' xe-8/0/0 ', ' xe-9/3/3 ']


def main():
    # Объявление глобальных переменных
    global switch_conf, router_conf, f_out
    global switch_ifd, switch_to_sw_ifd, router_ifl_regex, router_ifd

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
        # Создаём словарь r_vlans {ifl(ifd.unit): [VLAN]}
        r_vlans = {}
        for line in router_conf:
            for ifd in router_ifd:
                if 'set interfaces' + ifd in line and 'unit' in line:
                    # Для vlan-id
                    if ' vlan-id ' in line and 'input-vlan-map' not in line:
                        line = str(line).split(' ')
                        key = line[2].strip() + '.' + line[4].strip()
                        value = line[6].strip()
                        value = int(value.split()[-1])
                        if key not in r_vlans:
                            r_vlans.setdefault(key, []).append(value)
                        else:
                            r_vlans.key = value
                    # Для QinQ
                    elif 'vlan-tags outer' in line:
                        line = str(line).split(' ')
                        key = line[2].strip() + '.' + line[4].strip()
                        value = line[7].strip()
                        value = int(value.split()[-1])
                        if key not in r_vlans:
                            r_vlans.setdefault(key, []).append(value)
                        else:
                            r_vlans.key = value
        # print(r_vlans)

        # Находим общие значения двух словарей (VLANы) и создаём словарь r_sw_vlans {ifl(ifd.unit): [VLAN]}
        r_sw_vlans = {}
        for sw_k, sw_v in sw_vlans.items():
            for r_k, r_v in r_vlans.items():
                for i in sw_v:
                    for j in r_v:
                        if i == j:
                            r_v = ''.join(str(e) for e in r_v)
                            if r_k not in r_sw_vlans:
                                r_sw_vlans.setdefault(r_k, []).append(int(r_v))
                            else:
                                r_sw_vlans.r_k = int(r_v)
        # print(r_sw_vlans)

        # Находим все VLANы на физ. интерфейсах (ifd) коммутатора в сторону других коммутаторов
        # Создаём словарь sw_sw_vlans {ifd: [VLANs]}
        sw_sw_vlans = {}
        for line in switch_conf:
            for ifd in switch_to_sw_ifd:
                if ifd in line:
                    if 'vlan members' in line:
                        line = str(line).split(' ')
                        key = line[2].strip()
                        value = line[9].strip()
                        if '-' in value:
                            value = str(value).split('-')
                            value = list(range(int(value[0]), int(value[1])+1))
                        else:
                            value = int(value.split()[-1])
                        if key not in sw_sw_vlans:
                            sw_sw_vlans.setdefault(key, []).append(value)
                        else:
                            if isinstance(value, list):
                                for v in value:
                                    sw_sw_vlans[key].append(v)
                            else:
                                sw_sw_vlans[key].append(value)
        # print(sw_sw_vlans)

        # Сравниваем словарь r_sw_vlans и sw_sw_vlans
        for r_sw_k, r_sw_v in r_sw_vlans.items():
            # Если ifd смотрит на маршрутизатор, то выводим сразу
            if re.findall(router_ifl_regex, r_sw_k):
                print(r_sw_k, r_sw_v)
            else:
                # Или делаем проверку, что VLANы смотрят в сторону других коммутаторов
                for sw_sw_k, sw_sw_v in sw_sw_vlans.items():
                    if not re.findall(router_ifl_regex, r_sw_k):
                        for i in sw_sw_v:
                            for j in r_sw_v:
                                if i == j:
                                    print(r_sw_k, r_sw_v)


        sys.stdout = original
        # Only on stdout


if __name__ == "__main__":
    main()