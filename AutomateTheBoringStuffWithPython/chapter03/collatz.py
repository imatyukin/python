#!/usr/bin/env python3

result_collatz = 0

def main():

    global result_collatz

    while (result_collatz != 1):
        print("Введите целое число: ")
        try:
            number = int(input())
        except:
            print("Вы ввели нецелочисленное значение.")
            continue
        result_collatz = collatz(number)
        print(result_collatz)

    print("Возвращено значение 1.")

def collatz(number):
    if number % 2 == 0:
        return number // 2
    elif number % 2 == 1:
        return 3 * number + 1

if __name__ == "__main__":
    main()
