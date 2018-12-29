#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from urllib.request import urlopen

def get_request():
    with urlopen('http://127.0.0.1:8000/list') as net:
        data = net.read()
    print(data)

def post_request_s():
    post_data = 'Hello, world'.encode('utf-8')
    with urlopen('http://127.0.0.1:8000/subscribe', data=post_data) as net:
        data = net.read()
    print(data)

def post_request_w():
    people = [ 'Лукерья Власьевна', 'Татьяна Юрьевна', 'Пульхерия Андревна' ]
    post_data = pickle.dumps(people)
    with urlopen('http://127.0.0.1:8000/way', data=post_data) as net:
        data = net.read()
        people = pickle.loads(data)
    print(people)

#get_request()
post_request_w()
