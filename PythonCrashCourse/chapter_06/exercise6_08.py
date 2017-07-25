#!/usr/bin/env python3

nord = {
    'name': 'Норд',
    'kind of animal': 'собака',
    'owner': 'Человек',
    }

chapa = {
    'name': 'Чапа',
    'kind of animal': 'собака',
    'owner': 'Игорь',
    }

fish = {
    'name': '',
    'kind of animal': 'рыбы',
    'owner': 'Ирина',
    }

pets = [nord, chapa, fish]

for pet in pets:
    if pet['name'] == '':
        print("Вид животного: " + pet['kind of animal'])
        print("Имя владельца: " + pet['owner'])
        print("")
    else:
        print("Кличка домашнего животного: " + pet['name'])
        print("Вид животного: " + pet['kind of animal'])
        print("Имя владельца: " + pet['owner'])
        print("")