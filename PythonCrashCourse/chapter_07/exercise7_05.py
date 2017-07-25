#!/usr/bin/env python3

age = 0
while age != 'q':
    age = input("Введите возраст (или 'q'): ")
    if age.isdigit():
        age = int(age)
        if (age < 3):
            print("Для посетителей младше 3 лет билет бесплатный.")
        elif (age >= 3 and age <= 12):
            print("В возрасте от 3 до 12 билет стоит $10.")
        elif (age > 12):
            print("Если возраст посетителя больше 12, билет стоит $15.")
    else:
        if (age == 'q'):
            print("Программа завершена.")
        else:
            print("Неправильный ввод. Повторите попытку.")
