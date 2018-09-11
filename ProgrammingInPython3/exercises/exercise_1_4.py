#!/usr/bin/env python3
# 4. To make the awful poetry program more versatile, add some code to it so
#    that if the user enters a number on the command line (between 1 and 10
#    inclusive), the program will output that many lines. If no command-line
#    argument is given, default to printing five lines as before. You'll need to
#    change the main loop (e.g., to a while loop). Keep in mind that Python's
#    comparison operators can be chained, so there's no need to use logical and
#    when checking that the argument is in range. The additional functionality
#    can be done by adding about ten lines of code. A solution is provided as
#    awfulpoetry2_ans.py.

import sys
import random

try:
    if len(sys.argv) > 2:
        print("ОШИБКА -- количество аргументов командной строки больше одного")
        print(' '.join(sys.argv[0:]))
        exit(0)
    if len(sys.argv) == 1: sys.argv[1:] = [5]
    if int(sys.argv[1]) not in range(1, 11):
        print ("ОШИБКА -- аргумент должен быть числом от 1 до 10 включительно")
        print(' '.join(sys.argv[:2]))
        exit(0)

    articles = ["the", "a", "another"]
    subjects = ["cat", "dog", "man", "woman", "boy", "horse"]
    verbs = ["sang", "ran", "jumped", "laughed", "hoped"]
    adverbs = ["loudly", "quietly", "well", "badly", "rudely"]

    struct_1 = articles, subjects, verbs, adverbs
    struct_2 = articles, subjects, verbs

    struct = struct_1, struct_2

    for i in range(0, int(sys.argv[1])):
        sentence = ''
        for j in random.choice(struct):
            word = random.choice(j)
            sentence += ' ' + word
        print(sentence)
except ValueError as err:
    print ("ОШИБКА -- аргумент должен быть числом от 1 до 10 включительно")
    print(err, "in", "'" + sys.argv[0] + ' ' + sys.argv[1] + "'")