# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from pprint import pprint

access_dict = {}
trunk_dict = {}


def get_int_vlan_map(config_filename):
    file = open(config_filename, mode='r')
    all_of_it = file.read()
    with open(config_filename) as f:
        for conf_line in f:
            if 'interface FastEthernet' in conf_line:
                intf = str([fields.split()[1] for fields in conf_line.splitlines()])[2:-2]
                if 'interface ' + intf + '\n duplex auto' in all_of_it:
                    vlan = 1
                    access_dict[intf] = vlan
                if 'interface ' + intf + '\n switchport mode access\n duplex auto' in all_of_it:
                    vlan = 1
                    access_dict[intf] = vlan
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

file_name = 'config_sw2.txt'
access_cfg, trunk_cfg = get_int_vlan_map(file_name)
pprint(access_cfg)
pprint(trunk_cfg)
