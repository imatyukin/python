# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""

import yaml
from draw_network_graph import draw_topology

file_yaml = 'topology.yaml'


def unique_network_map(topology_dict):
    match_dict = {}
    base_keys = topology_dict.keys()
    for base_key in base_keys:
        match_values = match_dict.values()
        for key, value in topology_dict.items():
            if base_key not in match_values:
                if value not in match_dict.keys():
                    match_dict.update({(key, value)})
    return match_dict


def transform_topology(filename_yaml):
    with open(filename_yaml, "r") as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
            transform_dict = {}
            for key, value in parsed_yaml.items():
                for key1, value1 in value.items():
                    device = (key, key1)
                    for key2, value2 in value1.items():
                        neighbor = (key2, value2)
                        transform_dict[device] = neighbor
            return unique_network_map(transform_dict)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    draw_topology(transform_topology(file_yaml))
