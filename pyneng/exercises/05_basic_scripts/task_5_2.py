# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_net = input("Введите IP-сеть в формате <ip-network>/mask: ")
net, mask = ip_net.split('/')
net_list = net.split('.')
print("\nNetwork:")
print('{:<10}' '{:<10}' '{:<10}' '{:<10}'.format(net_list[0], net_list[1], net_list[2], net_list[3]))
print('  '.join([bin(int(x)+256)[3:] for x in net.split('.')]))
print("\nMask:")
print("/", mask, sep="")
cidr = int(mask)
mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
print('{:<10}' '{:<10}' '{:<10}' '{:<10}'.format(((0xff000000 & mask) >> 24),
                                          ((0x00ff0000 & mask) >> 16),
                                          ((0x0000ff00 & mask) >> 8),
                                          (0x000000ff & mask)))
print(bin(int((0xff000000 & mask) >> 24)+256)[3:],
      bin(int((0x00ff0000 & mask) >> 16)+256)[3:],
      bin(int((0x0000ff00 & mask) >> 8)+256)[3:],
      bin(int(0x000000ff & mask)+256)[3:], sep="  ")