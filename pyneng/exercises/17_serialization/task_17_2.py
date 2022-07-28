# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)
csv_file = "routers_inventory.csv"

headers = ["hostname", "ios", "image", "uptime"]


def parse_sh_version(sh_version):
    ios_regex = re.compile(r"(?<=Version ).(\d[\w.()]+)")
    ios = re.search(ios_regex, sh_version).group(0)
    image_regex = re.compile(r"(flash:|disk0:).*[a-zA-Z0-9]")
    image = re.search(image_regex, sh_version).group(0)
    uptime_regex = re.compile(r"(?<=router uptime is ).*")
    uptime = re.search(uptime_regex, sh_version).group(0)
    return ios, image, uptime


def write_inventory_to_csv(data_filenames, csv_filename):
    hostname_regex = re.compile(r".\d")
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    with open(csv_filename, 'a', newline='') as file_out:
        writer = csv.writer(file_out)
        for file in data_filenames:
            hostname = re.search(hostname_regex, file).group(0)
            data = []
            data.append(hostname)
            with open(file, 'r') as file_in:
                contents = file_in.read()
                ios, image, uptime = parse_sh_version(contents)
                data.append(ios)
                data.append(image)
                data.append(uptime)
                writer.writerow(data)


if __name__ == "__main__":
    write_inventory_to_csv(sh_version_files, csv_file)
