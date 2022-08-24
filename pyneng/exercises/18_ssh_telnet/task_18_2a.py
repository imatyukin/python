# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""

import yaml
from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)

commands = ["set system syslog file security authorization info", "set system syslog file messages authorization none",
            "set system syslog time-format year"]


def send_config_commands(device, config_commands, log=True):
    if log is True:
        try:
            with ConnectHandler(**device) as ssh:
                print('\nПодключаюсь к {}...\n'.format(device["host"]))
                output = ssh.send_config_set(config_commands, exit_config_mode=False)
                print(output)
                # Commit the config changes
                output = ssh.commit()
                print(output)
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            print('\nНе могу подключиться к {}...\n'.format(device["host"]))
            print(error)
    else:
        try:
            with ConnectHandler(**device) as ssh:
                ssh.send_config_set(config_commands, exit_config_mode=False)
                ssh.commit()
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            pass


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        send_config_commands(dev, commands, log=True)
