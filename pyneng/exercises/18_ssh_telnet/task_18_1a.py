# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""
import yaml
from netmiko import (ConnectHandler, NetmikoAuthenticationException)
from pprint import pprint


def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            output = ssh.send_command(command)
            return output
    except NetmikoAuthenticationException as error:
        print(error)


if __name__ == "__main__":
    command = "show interfaces terse"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_show_command(dev, command))
