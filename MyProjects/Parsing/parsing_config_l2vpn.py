#!/usr/bin/env python3

# Программа берёт unit'ы интерфейса связанные с encapsulation ccc из файла units
# и ищет строки, связанные с этими unit'ами, в файле interface, содержащем все настройки интерфейса.
from functools import reduce

# вывод команды: show configuration interfaces xe-2/3/0 | match ccc | display set
units = open('units', 'r').read()
# вывод команды: show configuration interfaces xe-2/3/0 | display set
interface = open('interface', 'r').read().splitlines()

# Находит пятое поле (номер подинтерфейса)
units = [fields.split()[4] for fields in units.splitlines()]
# Сортирует по значению (в арифметическом порядке)
units = [int(x) for x in units]
units.sort()
# Находит уникальные элементы в списке
unique_units = reduce(lambda l, x: l+[x] if x not in l else l, units, [])

# Находит в конфигурации интерфейса строки содержащие номер подинтерфейса
for line in interface:
    for unit in unique_units:
        if ' ' + str(unit) + ' ' in line:
            print(line)
