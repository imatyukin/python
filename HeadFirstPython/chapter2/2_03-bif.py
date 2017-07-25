#!/usr/bin/env python3

for num in range(4):
    print(num)
    
"""This is the "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
print(movies)

def print_lol(the_list, level):
    """This function takes a positional argument called "the_list", which
    is any Python list (of - possibly - nested lists). Each data item in the
    provided list is (recursively) printed to the screen on it's own line.
    A second argument called “level" is used to insert tab-stops when a nested list is encountered."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
            
print_lol(movies, 0)

names = ['John', 'Eric', ['Cleese', 'Idle'], 'Michael', ['Palin']]

def print_lol(the_list, level=0):
    '''optional arguments'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)

print_lol(names)
print_lol(names, 1)

def print_lol(the_list, ident=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, ident, level+1)
        else:
            if ident:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)

print_lol(names)
print_lol(names, True)
print_lol(names, True, 4)
