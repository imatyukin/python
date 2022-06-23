# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

import sys

ignore = ["duplex", "alias", "configuration"]

original_file = open(sys.argv[1], 'r')
revised_file = open(sys.argv[2], 'w')

for line in original_file:
    if line.startswith("!") is not True:
        if any(word in line for word in ignore) is not True:
            revised_file.write(line)

original_file.close()
revised_file.close()
