#!/usr/bin/env python3

filename = 'guest_book.txt'

name = input("Введите ваше имя: ")

while(name != 'q'):
    greeting = "Hello " + name + "!"
    print(greeting)
    with open(filename, 'a') as file_object:
        file_object.write(greeting + '\n')
    name = input("Введите ваше имя: ")
