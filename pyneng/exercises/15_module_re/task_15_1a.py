# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import re

file = "config_r1.txt"


def get_ip_from_cfg(filename):
    interfaces = []
    ip_addresses = []
    with open(filename) as f:
        f = f.readlines()
        pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        for line in f:
            if line.startswith("interface"):
                intf = (line.split())[1]
                interfaces.append(intf)
            if line.startswith(" no ip address") or line.startswith(" ip unnumbered"):
                ip = "temp_value"
                ip_addresses.append(ip)
            if line.startswith(" ip address "):
                ip = tuple((re.findall(pattern, line)))
                ip_addresses.append(ip)
        temp_ip_dict = list(zip(interfaces, ip_addresses))
        ip_dict = []
        for each in temp_ip_dict:
            if each[1] != 'temp_value':
                ip_dict.append(each)
    return dict(ip_dict)


if __name__ == "__main__":
    print(get_ip_from_cfg(file))
