#!/usr/bin/env python3

print("Введите два числа или 'q' для завершения.")

while True:

    first_number = str(input("\nПервое число: "))
    if first_number == 'q':
        break
    try:
        first_number = float(first_number)
    except (TypeError, ValueError):
        print ("Входное значение не является числом! Попробуйте снова.")
        continue

    second_number = str(input("\nВторое число: "))
    if second_number == 'q':
        break
    while True:
        try:
            if second_number == 'q':
                break
            second_number = float(second_number)
            break
        except (TypeError, ValueError):
            print("Входное значение не является числом! Попробуйте снова.")
            second_number = str(input("\nВторое число: "))
            continue

    if second_number == 'q':
        break
    answer = first_number + second_number
    print("\nРезультат сложения чисел: " + str(answer))