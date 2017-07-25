#!/usr/bin/env python3

'''Глава 8. Данные должны куда-то попадать'''
from test.test_io import CIncrementalNewlineDecoderTest

'''1. Присвойте строку 'This is a test of the emergency text system' переменной test1 
и запишите переменную test1 в файл с именем test.txt.'''

test1 = 'This is a test of the emergency text system'
fout = open('test.txt', 'wt')
fout.write(test1)
fout.close()

print('\n================================ RESTART ================================\n')

'''2. Откройте файл test.txt и считайте его содержимое в строку test2. Совпадают ли строки test1 и test2?'''

fin = open('test.txt', 'rt' )
test2 = fin.read()
fin.close()

print(len(test1) is len(test2))

print('\n================================ RESTART ================================\n')

'''3. Сохраните следующие несколько строк в файл books.csv. Обратите внимание на то, что, 
если поля разделены запятыми, вам нужно заключить поле в кавычки, если оно содержит запятую:
author,book
J R R Tolkien,The Hobbit
Lynne Truss,"Eats, Shoots & Leaves"'''

text = '''author,book
J R R Tolkien,The Hobbit
Lynne Truss,"Eats, Shoots & Leaves"
'''

with open('books.csv', 'wt') as fout:
    fout.write(text)

print('\n================================ RESTART ================================\n')

'''4. Используйте модуль csv и его метод DictReader, чтобы считать содержимое файла books.csv в переменную books. 
Выведите на экран значения переменной books. 
Обработал ли метод DictReader кавычки и запятые в заголовке второй книги?'''

import csv

with open('books.csv', 'rt') as fin:
    books = csv.DictReader(fin)
    for book in books:
        print(book)

print('\n================================ RESTART ================================\n')

'''5. Создайте CSV-файл books.csv и запишите его в следующие строки:
title,author,year
The Weirdstone of Brisingamen,Alan Garner,1960
Perdido Street Station,China Miéville,2000
Thud!,Terry Pratchett,2005
The Spellman Files,Lisa Lutz,2007
Small Gods,Terry Pratchett,1992'''

text = '''title,author,year
The Weirdstone of Brisingamen,Alan Garner,1960
Perdido Street Station,China Miéville,2000
Thud!,Terry Pratchett,2005
The Spellman Files,Lisa Lutz,2007
Small Gods,Terry Pratchett,1992
'''

import io

with io.open('books.csv', 'wt', encoding='utf8') as fout:
    fout.write(text)

print('\n================================ RESTART ================================\n')

'''6. Используйте модуль sqlite3, чтобы создать базу данных SQLite books.db и таблицу books, 
содержащую следующие поля: title (text), author (text) и year (integer).'''

import sqlite3

#db = sqlite3.connect('books.db')
#curs = db.cursor()
#curs.execute('''CREATE TABLE books (title TEXT, author TEXT, year INT)''')
#db.commit()
#db.close()

print('\n================================ RESTART ================================\n')

'''7. Считайте данные из файла books.csv и добавьте их в таблицу book.'''

#con = sqlite3.connect('books.db')
#cur = con.cursor()

#with io.open('books.csv','rt', encoding='utf8') as fin:
#    dr = csv.DictReader(fin)
#    to_db = [(i['title'], i['author'], i['year']) for i in dr]

#cur.executemany("INSERT INTO books (title, author, year) VALUES (?, ?, ?);", to_db)
#con.commit()
#con.close()

print('\n================================ RESTART ================================\n')

'''8. Считайте и выведите на экран графу title таблицы books в алфавитном порядке.'''

db = sqlite3.connect('books.db')
curs = db.cursor()
curs.execute('SELECT title FROM books ORDER BY title ASC')
rows = curs.fetchall()
print(rows)

print('\n')

sql = 'SELECT title FROM books ORDER BY title ASC'
for row in db.execute(sql):
    print(row)

print('\n')

for row in db.execute(sql):
    print(row[0])

print('\n')

sql = '''select title from books order by case when (title like "The %") then substr(title, 5) else title end'''
for row in db.execute(sql):
    print(row[0])

print('\n================================ RESTART ================================\n')

'''9. Считайте и выведите на экран все графы таблицы books в порядке публикации.'''

curs.execute('SELECT * FROM books ORDER BY year')
rows = curs.fetchall()
print(rows)

print('\n')

for row in db.execute('SELECT * FROM books ORDER BY year'):
    print(row)

print('\n')

for row in db.execute('SELECT * FROM books ORDER BY year'):
    print(*row, sep=', ')

db.close()

print('\n================================ RESTART ================================\n')

'''10. Используйте модуль sqlalchemy, чтобы подключиться к базе данных sqlite3 books.db, 
которую вы создали в упражнении 6. Как и в упражнении 8, 
считайте и выведите на экран графу title таблицы book в алфавитном порядке.'''

import sqlalchemy as sa

engine = sa.create_engine('sqlite:///books.db')
result = engine.execute('SELECT title FROM books ORDER BY title ASC')
for row in result:
    print(row)
result.close()

print('\n================================ RESTART ================================\n')

'''11. Установите сервер Redis и библиотеку Python redis (с помощью команды pip install redis) на свой компьютер. 
Создайте хеш redis с именем test, содержащий поля count (1) и name ('Fester Bestertester'). 
Выведите все поля хеша test.'''

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
print(r.set('foo', 'bar'))
print(r.get('foo'))

print('\n')

conn = redis.Redis('localhost')
print(conn.delete('test'))
print(conn.hmset('test', {'count': 1, 'name': 'Fester Bestertester'}))
print(conn.hgetall('test'))

print('\n================================ RESTART ================================\n')

'''12. Увеличьте поле count хеша test и выведите его на экран.'''

print(conn.hincrby('test', 'count', 3))
print(conn.hget('test', 'count'))
