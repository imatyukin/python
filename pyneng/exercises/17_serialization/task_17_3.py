# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re
from pprint import pprint

file_cfg = 'sh_cdp_n_sw1.txt'


def parse_sh_cdp_neighbors(sh_cdp_neighbors):
    hostname_regex = re.compile(r'.*(?=>)')
    hostname = re.search(hostname_regex, sh_cdp_neighbors).group(0)
    data = sh_cdp_neighbors.split("Port ID", 1)[1]
    data = "".join([s for s in data.splitlines(True) if s.strip("\r\n")])
    data = data.split('\n')[0:-1]
    cdp_dict = dict.fromkeys([hostname])
    temp2_dict = {}
    for elem in data:
        lintf_regex = re.compile(r'(\S+ \S+)(?=\s{2,})')
        lintf = re.search(lintf_regex, elem).group(0)
        deviceid_regex = re.compile(r'([^\s]+)')
        deviceid = re.search(deviceid_regex, elem).group(0)
        portid_regex = re.compile(r'(\S+ \S+)$')
        portid = re.search(portid_regex, elem).group(0)
        temp1_dict = {}
        temp1_dict[deviceid] = portid
        temp2_dict[lintf] = temp1_dict
        cdp_dict[hostname] = temp2_dict
    return cdp_dict


if __name__ == "__main__":
    with open(file_cfg, 'r') as f:
        contents = f.read()
        pprint(parse_sh_cdp_neighbors(contents))
