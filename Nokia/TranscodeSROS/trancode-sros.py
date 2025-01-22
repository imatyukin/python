#!/usr/bin/python3

# Скрипт для преобразования конфигурации SROS в плоский формат

import sys
import yaml

# Загрузка конфигурации из YAML файла
try:
    with open('config.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
        config_file_path = config.get('config_file_path', 'flat-config.txt')  # Путь к выходному файлу
        input_file_path = config.get('input_file_path', 'input.txt')  # Путь к входному файлу
except FileNotFoundError:
    print("Ошибка: Файл config.yaml не найден.")
    sys.exit(1)

# Открытие входного файла
try:
    with open(input_file_path, 'r') as file_cfg:
        lines = file_cfg.readlines()
except FileNotFoundError:
    print(f"Ошибка: Входной файл {input_file_path} не найден.")
    sys.exit(1)

# Инициализация переменных
tab_LINE = []
index = 0
last_indentation = 0
indentation = 0
exit_found = False

# Открытие выходного файла для записи
with open(config_file_path, 'w') as output_file:
    for line in lines:
        # Пропуск строк с разделителями, комментариями и пустых строк
        if line.strip().startswith(('---', '===', '#', 'echo')) or line.strip() == '':
            continue

        # Пропуск команды 'exit all'
        if line.strip() == 'exit all':
            continue

        # Обработка строк конфигурации
        if line.strip() != '':
            # Определение уровня вложенности
            indentation = line.count('    ')

            # Обработка строк, не содержащих 'exit'
            if line.strip() != 'exit':
                # Если текущая строка более вложенная, чем предыдущая, добавляем её в список
                if (indentation > last_indentation) or indentation == 0:
                    # Добавляем '/' для команды 'configure'
                    if line.strip() == 'configure':
                        line = '/' + line
                    # Обработка строк с 'create'
                    if 'create' in line.strip():
                        create_line = ' '.join(tab_LINE) + ' ' + line.strip()
                        print(create_line)  # Вывод на экран
                        output_file.write(create_line + '\n')  # Запись в файл
                        line = line.replace(' create', '').strip()
                    if index > 0 and 'create' in tab_LINE[index - 1]:
                        print(' '.join(tab_LINE))  # Вывод на экран
                        output_file.write(' '.join(tab_LINE) + '\n')  # Запись в файл
                        tab_LINE[index - 1] = tab_LINE[index - 1].replace(' create', '')

                    tab_LINE.append(line.strip())
                    index += 1
                    exit_found = False
                # Если текущая строка менее вложенная, удаляем последний элемент из списка
                if indentation < last_indentation:
                    del tab_LINE[index - 1]
                    tab_LINE.append(line.strip())
                # Если текущая строка на том же уровне вложенности
                if (last_indentation == indentation) and indentation != 0:
                    if exit_found:
                        del tab_LINE[index - 1]
                        tab_LINE.append(line.strip())
                        print(' '.join(tab_LINE))  # Вывод на экран
                        output_file.write(' '.join(tab_LINE) + '\n')  # Запись в файл
                    else:
                        print(' '.join(tab_LINE))  # Вывод на экран
                        output_file.write(' '.join(tab_LINE) + '\n')  # Запись в файл
                        del tab_LINE[index - 1]
                        tab_LINE.append(line.strip())
                last_indentation = indentation

            # Обработка строк с 'exit'
            else:
                if not exit_found:
                    if last_indentation != indentation:
                        print(' '.join(tab_LINE))  # Вывод на экран
                        output_file.write(' '.join(tab_LINE) + '\n')  # Запись в файл
                        del tab_LINE[index - 1]
                        index -= 1
                        del tab_LINE[index - 1]
                        index -= 1
                        last_indentation = indentation - 1
                        exit_found = True
                    else:
                        exit_found = False
                else:
                    del tab_LINE[index - 1]
                    index -= 1
                    last_indentation = indentation - 1

print(f"Конфигурация успешно сохранена в файл: {config_file_path}")