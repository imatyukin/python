#!/usr/bin/env python3

filename = 'learning_python.txt'

with open(filename) as file_object:
    lines = file_object.readlines()
    for message in lines:
        print(message.replace('Python', 'C').rstrip())
