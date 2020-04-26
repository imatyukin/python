#!/usr/bin/env python3
# 2. IDLE can be used as a very powerful and flexible calculator, but sometimes
#    it is useful to have a task-specific calculator. Create a program that
#    prompts the user to enter a number in a while loop, gradually building
#    up a list of the numbers entered. When the user has finished (by simply
#    pressing Enter), print out the numbers they entered, the count of numbers,
#    the sum of the numbers, the lowest and highest numbers entered, and the
#    mean of the numbers (sum / count). Here is a sample run:
#
#       average1_ans.py
#       enter a number or Enter to finish: 5
#       enter a number or Enter to finish: 4
#       enter a number or Enter to finish: 1
#       enter a number or Enter to finish: 8
#       enter a number or Enter to finish: 5
#       enter a number or Enter to finish: 2
#       enter a number or Enter to finish:
#       numbers: [5, 4, 1, 8, 5, 2]
#       count = 6 sum = 25 lowest = 1 highest = 8 mean = 4.16666666667
#
#    It will take about four lines to initialize the necessary variables (an empty
#    list is simply []), and less than 15 lines for the while loop, including basic
#    error handling. Printing out at the end can be done in just a few lines, so
#    the whole program, including blank lines for the sake of clarity, should be
#    about 25 lines.

prompt = 'enter a number or Enter to finish: '
numbers = []
count = sum = 0
lowest = None
highest = None

mean = number = input(prompt)

while(number):
    try:
        if lowest is None or lowest > int(number):
            lowest = int(number)
        if highest is None or highest < int(number):
            highest = int(number)
        numbers.append(int(number))
        count += 1
        sum += int(number)
        number = input(prompt)
    except ValueError as err:
        print(err)
        lowest = None
        highest = None
        number = input(prompt)

mean = sum / count

print('numbers:', numbers)
print('count =', count, 'sum =', sum, 'lowest =', lowest, 'highest =', highest, 'mean =', mean)