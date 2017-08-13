#!/usr/bin/env python3

filename = 'guest.txt'

name = input("Введите ваше имя: ")

with open(filename, 'w') as file_object:
    file_object.write(name)
