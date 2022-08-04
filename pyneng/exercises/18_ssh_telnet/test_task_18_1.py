import sys

import task_18_1

sys.path.append("..")

from pyneng_common_functions import (check_function_exists, check_pytest,
                                     strip_empty_lines)

check_pytest(__loader__, __file__)


def test_functions_created():
    """
    Проверка, что функция создана
    """
    check_function_exists(task_18_1, "send_show_command")


def test_function_return_value(r1_test_connection, first_router_from_devices_yaml):
    """
    Тест проверяет работу функции send_show_command
    first_router_from_devices_yaml - это первое устройство из файла devices.yaml
    r1_test_connection - это сессия SSH с первым устройством из файла devices.yaml
                         Используется для проверки вывода
    """
    correct_return_value = strip_empty_lines(
        r1_test_connection.send_command("show interfaces terse")
    )
    return_value = strip_empty_lines(
        task_18_1.send_show_command(first_router_from_devices_yaml, "show interfaces terse")
    )
    assert return_value is not None, "Функция ничего не возвращает"
    assert (
        type(return_value) == str
    ), f"По заданию функция должна возвращать строку, а возвращает {type(return_value).__name__}"
    assert (
        correct_return_value == return_value
    ), "Функция возвращает неправильное значение"


def test_function_return_value_different_args(
    r1_test_connection, first_router_from_devices_yaml
):
    """
    Проверка работы функции с другими аргументами
    """
    correct_return_value = strip_empty_lines(
        r1_test_connection.send_command("show interfaces descriptions")
    )
    return_value = strip_empty_lines(
        task_18_1.send_show_command(
            first_router_from_devices_yaml, "show interfaces descriptions"
        )
    )
    assert return_value is not None, "Функция ничего не возвращает"
    assert (
        type(return_value) == str
    ), f"По заданию функция должна возвращать строку, а возвращает {type(return_value).__name__}"
    assert (
        correct_return_value == return_value
    ), "Функция возвращает неправильное значение"
