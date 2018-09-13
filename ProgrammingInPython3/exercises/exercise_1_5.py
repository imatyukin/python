#!/usr/bin/env python3
# 5. It would be nice to be able to calculate the median (middle value) as well
#    as the mean for the averages program in Exercise 2, but to do this we must
#    sort the list. In Python a list can easily be sorted using the list.sort()
#    method, but we haven’t covered that yet, so we won’t use it here. Extend
#    the averages program with a block of code that sorts the list of
#    numbers—efficiency is of no concern, just use the easiest approach you
#    can think of. Once the list is sorted, the median is the middle value if the
#    list has an odd number of items, or the average of the two middle values
#    if the list has an even number of items. Calculate the median and output
#    that along with the other information.
#
#    This is rather tricky, especially for inexperienced programmers. If you
#    have some Python experience,you might still find it challenging, at least if
#    you keep to the constraint of using only the Python we have covered so far.
#    The sorting can be done in about a dozen lines and the median calculation
#    (where you can’t use the modulus operator, since it hasn’t been covered yet)
#    in four lines. A solution is provided in average2_ans.py.

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


# Сортировка методом пузырька
n = 1
while n < len(numbers):
    for i in range(len(numbers)-n):
        if numbers[i] > numbers[i+1]:
            numbers[i], numbers[i+1] = numbers[i+1], numbers[i]
    n += 1
print('sorted numbers:', numbers)

half = int(len(numbers)/2)
if len(numbers)/2 == half:
    print('median =', (numbers[half-1]+numbers[half])/2)
else:
    print('median =', int(numbers[half]))