#!/usr/bin/env python3

num_of_seats = input("На сколько мест вы хотите забронировать стол в ресторане? ")
num_of_seats = int(num_of_seats)

if (num_of_seats > 8):
    print("Вам придётся подождать.")
else:
    print("Стол готов.")