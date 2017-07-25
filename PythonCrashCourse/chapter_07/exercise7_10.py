#!/usr/bin/env python3

gender = {}
responses_male = {}
responses_female = {}

polling_active = True

while polling_active:
    name = input("Ваше имя? ")
    while True:
        sex = input("Ваш пол (м/ж)? ")
        if (sex == 'м'):
            response_male = input("Где бы вы хотели провести отпуск? ")
            break
        elif (sex == 'ж'):
            response_female = input("Где бы вы хотели провести отпуск? ")
            break
        else:
            print("Вы не указали ваш пол. Повторите попытку.")
            continue

    gender[sex] = name
    for sex, name in gender.items():
        if (sex == 'м'):
            responses_male[name] = response_male
        if (sex == 'ж'):
            responses_female[name] = response_female

    while True:
        repeat = input("Вы хотите продолжить опрос пользователей? (да/нет) ")
        if (repeat == 'да'):
            break
        elif (repeat == 'нет'):
            polling_active = False
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")
            continue

print("\n--- Результаты опроса ---")
for name, response_male in responses_male.items():
    print("Место, где хотел бы провести отпуск " + name + " - " + response_male + ".")
for name, response_female in responses_female.items():
    print("Место, где хотела бы провести отпуск " + name + " - " + response_female + ".")
