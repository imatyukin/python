#!/usr/bin/env python3

'''Глава 10. Системы'''

'''1. Запишите текущие дату и время как строку в текстовый файл today.txt.'''

from datetime import datetime, date
now = datetime.now()
now_str = str(datetime.now())

fout = open('today.txt', 'wt')
fout.write(now_str)
fout.close()

print('\n================================ RESTART ================================\n')

'''2. Прочтите текстовый файл today.txt и разместите данные в строке today_string.'''

fin = open('today.txt', 'rt' )
today_string = fin.read()
fin.close()

print(today_string)

print('\n================================ RESTART ================================\n')

'''3. Разберите дату из строки today_string.'''

this_day = date.today()
print("This date is", this_day)
print("This year is", now.year)
print("This month is", now.month)
print("This day is", now.day)

print('\n================================ RESTART ================================\n')

'''4. Выведите на экран список файлов текущего каталога.'''

import os

print(os.listdir('.'))

print('\n================================ RESTART ================================\n')

'''5. Выведите на экран список файлов родительского каталога.'''

print(os.listdir('..'))

print('\n================================ RESTART ================================\n')

'''6. Используйте модуль multiprocessing, чтобы создать три отдельных процесса. 
Заставьте каждый из них ждать случайное количество секунд (от одной до пяти), 
вывести текущее время и завершить работу.'''

import multiprocessing
from random import randint
import time

def whoami(what):
    print("Process %s is %s" % (os.getpid(), what))

if __name__ == "__main__":
    for i in range(3):
        p = multiprocessing.Process(target=whoami, args=("number %s" % i,))
        p.start()
        time.sleep(randint(1,5))
        fmt = "Time: %H:%M:%S"
        t = time.localtime()
        print(time.strftime(fmt, t))
        p.terminate()

print('\n================================ RESTART ================================\n')

'''7. Создайте объект date, содержащий дату вашего рождения.'''

date = date(1979, 7, 26)
print(date)

print('\n================================ RESTART ================================\n')

'''8. В какой день недели вы родились?'''

print(date.strftime("%A"))

print('\n================================ RESTART ================================\n')

'''9. Когда вам будет (или уже было) 10 000 дней от роду?'''

from datetime import timedelta

ten_thousand_days = timedelta(days=10000)
sometime = date + ten_thousand_days
print(sometime)

