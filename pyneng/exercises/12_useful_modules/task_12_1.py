# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


import platform
import subprocess


ip_addresses = ["127.0.0.1", "100.123.0.1", "198.18.1.1"]


def ping_ip_addresses(ip_addresses):
    alive = []
    dead = []
    for ip in ip_addresses:
        parameter = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', parameter, '1', ip]
        response = subprocess.call(command)

        if response == 0:
            alive.append(ip)
        else:
            dead.append(ip)
    return alive, dead


if __name__ == "__main__":
    alive, unreach = ping_ip_addresses(ip_addresses)
    print("\nСписок доступных IP-адресов:", ', '.join(str(x) for x in alive))
    print("Список недоступных IP-адресов:", ', '.join(str(x) for x in unreach))
