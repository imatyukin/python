# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import re
ip_addr = input("Введите IP-адрес: ")
match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip_addr)
ip_addr_s = ip_addr.split(".")
if bool(match) is True and all((int(part) > -1 and int(part)) < 256 for part in ip_addr_s):
    if ip_addr == '255.255.255.255':
        print('local broadcast')
    elif ip_addr == '0.0.0.0':
        print('unassigned')
    elif int(ip_addr.split(".")[0]) in range(1, 224):
        print('unicast')
    elif int(ip_addr.split(".")[0]) in range(224, 240):
        print('multicast')
    else:
        print('unused')
else:
    print("Неправильный IP-адрес")
