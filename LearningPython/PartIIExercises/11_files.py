#!/usr/bin/env python3

# Creates a new output file and writes the string
with open('myfile.txt', 'w') as file:
    file.write("Hello file world!\n")
# Opens myfile.txt and reads and prints its contents
with open('myfile.txt') as file:
    print(file.read())
