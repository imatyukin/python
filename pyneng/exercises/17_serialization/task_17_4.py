# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""

import datetime
import csv
import re

log = 'mail_log.csv'
output = 'result.csv'


def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def convert_datetime_to_str(datetime_obj):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")


def write_last_log_to_csv(source_log, output):
    date_regex = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}')
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    with open(source_log, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        base = {}
        for row in reader:
            try:
                date = re.search(date_regex, ', '.join(row)).group(0)
                email = re.search(email_regex, ', '.join(row)).group(0)
            except AttributeError:
                date = re.match(date_regex, ', '.join(row))
                email = re.match(email_regex, ', '.join(row))
            if len(row) > 0:
                if email is not None:
                    if email in base:
                        del row[1]
                        date = convert_str_to_datetime(date)
                        row[1] = date
                        base[email].append(row)
                    else:
                        del row[1]
                        date = convert_str_to_datetime(date)
                        row[1] = date
                        base[email] = [row]
        result = {}
        for k, v in base.items():
            max_value = max(v, key=lambda x: x[1])
            date = convert_datetime_to_str(max_value[1])
            max_value[1] = date
            result[k] = max_value
        headers = ['Name', 'Email', 'Last Changed']
        with open(output, 'w', newline='') as csvresult:
            writer = csv.writer(csvresult)
            writer.writerow(headers)
            for k, v in result.items():
                v.append(k)
                v[1], v[2] = v[2], v[1]
                writer.writerow(v)


if __name__ == "__main__":
    write_last_log_to_csv(log, output)
