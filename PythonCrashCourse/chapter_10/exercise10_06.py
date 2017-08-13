#!/usr/bin/env python3

print("Введите два числа\n")

try:
    first_number = float(input("Первое число: "))
except (TypeError, ValueError):
    print ("Входное значение не является числом! Попробуйте снова.")
    first_number = float(input("Первое число: "))

try:
    second_number = float(input("Второе число: "))
except (TypeError, ValueError):
    print ("Входное значение не является числом! Попробуйте снова.")
    second_number = float(input("Второе число: "))

answer = first_number + second_number
print("\nРезультат сложения чисел: " + str(answer))