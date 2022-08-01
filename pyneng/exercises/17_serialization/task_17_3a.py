# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""

import glob
import re
from pprint import pprint
import yaml

list_of_files = glob.glob("sh_cdp_n_*")
save_to_filename = 'topology.yaml'


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    cdp_full_dict = {}
    for file_name in list_of_files:
        with open(file_name, 'r') as f:
            contents = f.read()
            hostname_regex = re.compile(r'.*(?=>)')
            hostname = re.search(hostname_regex, contents).group(0)
            data = contents.split("Port ID", 1)[1]
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
                cdp_full_dict.update(cdp_dict)
    if save_to_filename != None:
        with open(save_to_filename, 'w') as outfile:
            yaml.dump(cdp_full_dict, outfile, default_flow_style=False)
    return cdp_full_dict


if __name__ == "__main__":
    pprint(generate_topology_from_cdp(list_of_files, save_to_filename=None))
