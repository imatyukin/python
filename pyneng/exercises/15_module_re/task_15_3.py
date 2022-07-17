# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re

cfg_ios = 'cisco_nat_config.txt'
cfg_asa = 'asa_nat_config.txt'


def convert_ios_nat_to_asa(cfg_ios_nat, cfg_asa_nat):
    with open(cfg_ios_nat) as ci:
        with open(cfg_asa_nat, 'w') as ca:
            for line in ci:
                ip_addr = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                ip_addr = str(re.findall(ip_addr, line))[2:-2]
                port_in = re.compile(r' \d+ ')
                port_in = str(re.findall(port_in, line))[3:-2]
                port_out = re.compile(r'\d+$')
                port_out = str(re.findall(port_out, line))[2:-2]
                ca.write("object network LOCAL_" + ip_addr + "\n")
                ca.write(" host " + ip_addr + "\n")
                ca.write(" nat (inside,outside) static interface service tcp " + port_in + port_out + "\n")


if __name__ == "__main__":
    convert_ios_nat_to_asa(cfg_ios, cfg_asa)
