# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

vlan = input("Enter VLAN number: ")

with open("CAM_table.txt") as f:
    lst = []
    for line in f:
        if len(line) > 2:
            if line[1].isdigit():
                lst.append(line.split())

for x in lst:
    x[0] = int(x[0])
lst = sorted(lst)
for x in lst:
    x[0] = str(x[0])

for i in lst:
    if " ".join(i).split()[0] == vlan:
        print('{:9}''{:20}''{}'.format(" ".join(i).split()[0], " ".join(i).split()[1], " ".join(i).split()[3]))
