#!/usr/bin/env python3

'''Глава 11. Конкуренция и сети'''

'''1. Используйте объект класса socket, чтобы реализовать службу, сообщающую текущее время. 
Когда клиент отправляет на сервер строку 'time', верните текущие дату и время как строку ISO.'''

'''from datetime import datetime
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 6789
print('Waiting for a client on', host, 'port', port)
serversocket.bind((host, port))

max_size = 1024

while True:
    data, client_addr = serversocket.recvfrom(max_size)
    print(client_addr, 'asked', data.decode('UTF-8'))
    if data == b'time':
        dtnow = str(datetime.utcnow())
        serversocket.sendto(dtnow.encode(encoding='utf_8'), client_addr)
        print('Server sent', data.decode('UTF-8'))

serversocket.close()'''

print('\n================================ RESTART ================================\n')

'''2. Используйте сокеты ZeroMQ REQ и REP, чтобы сделать то же самое.'''

'''import zmq

host = '127.0.0.1'
port = 6789
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://%s:%s" % (host, port))

print('Server started at', datetime.utcnow())

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request:", message.decode('UTF-8'))
    if message == b'time':
        dtnow = str(datetime.utcnow())
        socket.send(bytes(dtnow, 'utf-8'))
        print('Server sent', dtnow)'''

print('\n================================ RESTART ================================\n')

'''3. Попробуйте сделать то же самое с помощью XMLRPC.'''

'''from xmlrpc.server import SimpleXMLRPCServer

def getCurrentTime():
    data = str(datetime.utcnow())
    print('Server sent', data)
    return data

print('Serving XML-RPC on localhost port 6789')
server = SimpleXMLRPCServer(("localhost", 6789))
server.register_function(getCurrentTime, "getCurrentTime")
server.serve_forever()'''

print('\n================================ RESTART ================================\n')

'''4. Возможно, вы видели эпизод телесериала I Love Lucy, в котором Люси и Этель работают на шоколадной фабрике 
(это классика). Парочка стала отставать, когда линия конвейера, которая направляла к ним на обработку конфеты, 
начала работать еще быстрее. Напишите симуляцию, которая отправляет разные типы конфет в список Redis, 
и клиент Lucy, который делает блокирующие выталкивания из списка. Ей нужно 0,5 секунды, чтобы обработать одну 
конфету. Выведите на экран время и тип каждой конфеты, которую получит Lucy, а также количество необработанных 
конфет.'''

'''nohup redis-server &'''

'''import redis
import random
from time import sleep

r = redis.StrictRedis(host='localhost', port=6379, db=0)

candies = ['Cadbury', 'Dark chocolate', 'Hershey Bar', 'Hershey\'s Kisses', 'Jersey Milk', 'Kit Kat', 'Lindt', \
      'Maltesers', 'Milk Duds', 'Milky Way', 'Peppermint bark', 'Reese\'s Peanut Butter Cup', 'Rolo', \
      'Snickers', 'Twix', 'Whoppers']
conveyor = 'chocolates'

while True:
    seconds = random.random()
    sleep(seconds)
    piece = random.choice(candies)
    r.rpush(conveyor, piece)'''

print('\n================================ RESTART ================================\n')

'''5. Используйте ZeroMQ, чтобы публиковать стихотворение из упражнения 7 главы 7 по одному слову за раз. 
Напишите потребителя ZeroMQ, который будет выводить на экран каждое слово, начинающееся с гласной. 
Напишите другого потребителя, который будет выводить все слова, состоящие из пяти букв. 
Знаки препинания игнорируйте.'''

import zmq
import string
from time import sleep

host = '*'
port = 6789
ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
pub.bind('tcp://%s:%s' % (host, port))

sleep(1)

mammoth = '''
We have seen thee, queen of cheese,
Lying quietly at your ease,
Gently fanned by evening breeze,
Thy fair form no flies dare seize.
All gaily dressed soon you'll go
To the great Provincial show,
To be admired by many a beau
In the city of Toronto.
Cows numerous as a swarm of bees,
Or as the leaves upon the trees,
It did require to make thee please,
And stand unrivalled, queen of cheese.
May you not receive a scar as
We have heard that Mr. Harris
Intends to send you off as far as
The great world's show at Paris.
Of the youth beware of these,
For some of them might rudely squeeze
And bite your cheek, then songs or glees
We could not sing, oh! queen of cheese.
We'rt thou suspended from balloon,
You'd cast a shade even at noon,
Folks would think it was the moon
About to fall and crush them soon.
... '''

for word in mammoth.split():
    word = word.strip(string.punctuation)
    data = word.encode('utf-8')
    if word.startswith(('a','e','i','o','u','A','E','I','O','U')):
        pub.send_multipart([b'vowels', data])
    if len(word) == 5:
        pub.send_multipart([b'five', data])
