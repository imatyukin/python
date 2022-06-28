# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from pprint import pprint

access_dict = {}
trunk_dict = {}


def get_int_vlan_map(config_filename):
    with open(config_filename) as f:
        for conf_line in f:
            if 'interface FastEthernet' in conf_line:
                intf = str([fields.split()[1] for fields in conf_line.splitlines()])[2:-2]
            if 'switchport access vlan' in conf_line:
                vlan = str([fields.split()[3] for fields in conf_line.splitlines()])[2:-2]
                access_dict[intf] = int(vlan)
            if 'switchport trunk allowed vlan' in conf_line:
                vlans = str([fields.split()[4] for fields in conf_line.splitlines()])[2:-2]
                vlans = list(map(int, vlans.split(",")))
                trunk_dict[intf] = vlans

    return access_dict, trunk_dict


file_name = 'config_sw1.txt'
access_cfg, trunk_cfg = get_int_vlan_map(file_name)
pprint(access_cfg)
pprint(trunk_cfg)
