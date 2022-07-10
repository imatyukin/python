# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""


import ipaddress


ips = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']


def convert_ranges_to_ip_list(ip_addr):
    ip_list = []
    for ip in ip_addr:
        if "-" in ip:
            ip = ip.split("-")
            if "." in ip[1]:
                subip = lambda x: ['.'.join(i.split('.')[3:]) for i in x]
                for start_ip, full_start_ip in zip(subip(ip[0:1]), ip[0:1]):
                    for end_ip, full_end_ip in zip(subip(ip[1:2]), ip[1:2]):
                        full_start_ip = ipaddress.IPv4Address(full_start_ip)
                        full_end_ip = ipaddress.IPv4Address(full_end_ip)
                        for ip_int in range(int(full_start_ip), int(full_end_ip)+1):
                            ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            else:
                subip = lambda x: ['.'.join(i.split('.')[:3]) for i in x]
                for start_ip, full_start_ip in zip(subip(ip[0:1]), ip[0:1]):
                    full_end_ip = start_ip + "." + ip[1]
                    full_start_ip = ipaddress.IPv4Address(full_start_ip)
                    full_end_ip = ipaddress.IPv4Address(full_end_ip)
                    for ip_int in range(int(full_start_ip), int(full_end_ip)+1):
                        ip_list.append(str(ipaddress.IPv4Address(ip_int)))
        else:
            ip_list.append(ip)
    return ip_list


if __name__ == "__main__":
    print(convert_ranges_to_ip_list(ips))
