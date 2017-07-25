#!/usr/bin/env python3

'''Глава 11. Конкуренция и сети'''

'''1. Используйте объект класса socket, чтобы реализовать службу, сообщающую текущее время. 
Когда клиент отправляет на сервер строку 'time', верните текущие дату и время как строку ISO.'''

'''import socket
from datetime import datetime
from time import sleep

address = ('localhost', 6789)
max_size = 1024

print('Starting the client at', datetime.now())

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sleep(5)
    client.sendto(b'time', address)
    data, server_addr = client.recvfrom(max_size)
    print('Client read', data.decode('UTF-8'))

client.close()'''

print('\n================================ RESTART ================================\n')

'''2. Используйте сокеты ZeroMQ REQ и REP, чтобы сделать то же самое.'''

'''import zmq

host = '127.0.0.1'
port = 6789
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://%s:%s" % (host, port))
print("Connecting to server...")

while True:
    sleep(5)
    request_str = 'time'
    request_bytes = request_str.encode('utf-8')
    socket.send(request_bytes)
    reply = socket.recv()
    reply_str = reply.decode('utf-8')
    print("Sent %s, received %s" % (request_str, reply_str))'''

print('\n================================ RESTART ================================\n')

'''3. Попробуйте сделать то же самое с помощью XMLRPC.'''

'''import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:6789/")
while True:
    sleep(5)
    result = proxy.getCurrentTime()
    print("Client received %s" % result)'''

print('\n================================ RESTART ================================\n')

'''4. Возможно, вы видели эпизод телесериала I Love Lucy, в котором Люси и Этель работают на шоколадной фабрике 
(это классика). Парочка стала отставать, когда линия конвейера, которая направляла к ним на обработку конфеты, 
начала работать еще быстрее. Напишите симуляцию, которая отправляет разные типы конфет в список Redis, 
и клиент Lucy, который делает блокирующие выталкивания из списка. Ей нужно 0,5 секунды, чтобы обработать одну 
конфету. Выведите на экран время и тип каждой конфеты, которую получит Lucy, а также количество необработанных 
конфет.'''

'''import redis
from datetime import datetime
from time import sleep

r = redis.StrictRedis(host='localhost', port=6379, db=0)

timeout = 10
conveyor = 'chocolates'

while True:
    sleep(0.5)
    msg = r.blpop(conveyor, timeout)
    remaining = r.llen(conveyor)
    if msg:
        piece = msg[1]
        print('Lucy got a', piece.decode('utf-8'), 'at', datetime.now(),
              ', only', remaining, 'left')'''

print('\n================================ RESTART ================================\n')

'''5. Используйте ZeroMQ, чтобы публиковать стихотворение из упражнения 7 главы 7 по одному слову за раз. 
Напишите потребителя ZeroMQ, который будет выводить на экран каждое слово, начинающееся с гласной. 
Напишите другого потребителя, который будет выводить все слова, состоящие из пяти букв. 
Знаки препинания игнорируйте.'''

import zmq
import string

host = '127.0.0.1'
port = 6789
ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.connect('tcp://%s:%s' % (host, port))
sub.setsockopt(zmq.SUBSCRIBE, b'vowels')
sub.setsockopt(zmq.SUBSCRIBE, b'five')

while True:
    topic, word = sub.recv_multipart()
    print('Topic:', topic.decode('utf-8'), '-', 'Word:', word.decode('utf-8'))
