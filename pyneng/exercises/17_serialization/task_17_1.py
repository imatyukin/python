# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""

import re
import csv

files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
output = 'output.csv'


def write_dhcp_snooping_to_csv(filenames, output):
    titles = ['switch', 'mac', 'ip', 'vlan', 'interface']
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(titles)
    name_regex = re.compile(r"^[^_]*")
    for file in filenames:
        fname = re.search(name_regex, file).group(0)
        with open(file, 'r') as file_in, open(output, 'a', newline='') as file_out:
            writer = csv.writer(file_out)
            for line in file_in:
                mac_regex = re.compile(r"^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})")
                if mac_regex.match(line):
                    mac = re.search(mac_regex, line).group(0)
                    if line.startswith(mac):
                        rows = []
                        list_elem = line.split(" ")
                        filter_elem = list(filter(None, list_elem))
                        rows.append(fname)
                        del filter_elem[2:4]
                        for item in filter_elem:
                            if '\n' in item:
                                item = item.strip('\n')
                                rows.append(item)
                            else:
                                rows.append(item)
                        writer.writerow(rows)


if __name__ == "__main__":
    print(write_dhcp_snooping_to_csv(files, output))
