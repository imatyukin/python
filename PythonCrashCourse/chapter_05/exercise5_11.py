#!/usr/bin/env python3

digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for digit in digits:
    if (digit == 1):
        print(str(1) + "st")
    if (digit == 2):
        print(str(2) + "nd")
    if (digit == 3):
        print(str(3) + "rd")
    elif digit in range(4, 10):
        print(str(digit) + "th")
