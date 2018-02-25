#!/usr/bin/env python3

def NewString(arg):
    all_elements_except_last = ', '.join(arg[:-1])
    last_element = str(arg[-1])
    print(all_elements_except_last + ', and ' + last_element)

spam = ['apples', 'bananas', 'tofu', 'cats']
NewString(spam)
