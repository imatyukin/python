# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""

import re
from pprint import pprint

filename = "sh_ip_int_br.txt"


def parse_sh_ip_int_br(filename):
    ip_list = []
    port = re.compile(r'^[A-Z]\w+/?\d')
    ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|unassigned')
    stat = re.compile(r'up|down|administratively down')
    proto = re.compile(r'up|down')
    with open(filename) as f:
        for line in f:
            intf = str(re.findall(port, line))[2:-2]
            ip_addr = str(re.findall(ip, line))[2:-2]
            status = re.findall(stat, line)
            protocol = re.findall(proto, line)
            if status != [] and protocol != []:
                status = re.findall(stat, line)[0]
                protocol = re.findall(proto, line)[1]
            if intf != '' and ip_addr != '':
                data = tuple([intf, ip_addr, status, protocol])
                ip_list.append(data)
    return ip_list


if __name__ == "__main__":
    pprint(parse_sh_ip_int_br(filename))
