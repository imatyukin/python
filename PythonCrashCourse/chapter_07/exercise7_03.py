#!/usr/bin/env python3

number = 0
while number != 'quit':
    number = input("Введите число (или 'quit'): ")
    if number.isdigit():
        number = int(number)
        if (number % 10 == 0):
            print("Число " + str(number) + " кратно 10.")
        else:
            print("Число " + str(number) + " не кратно 10.")
    else:
        if number == 'quit':
            print("Программа завершена.")
        else:
            print("Неправильный ввод. Повторите попытку.")
