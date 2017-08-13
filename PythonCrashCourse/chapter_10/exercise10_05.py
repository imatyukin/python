#!/usr/bin/env python3

filename = 'love_programming.txt'
flag = 2

def check_duplicate(answer, flag):
    with open(filename) as file_object:
        for line in file_object:
            line = line.rstrip()
            if line == answer:
                flag = 0
    if flag == 0:
        return 0
    else:
        return 1

while(1):
    if flag == 2:
        answer = input("Why do you love programming?\n")
        if answer == 'q':
            print("\nExit")
            break
        else:
            with open(filename, 'w') as file_object:
                file_object.write(answer + '\n')
            flag = 1
            continue
    else:
        answer = input("Why do you love programming?\n")
        if answer == 'q':
            print("\nExit")
            break
        else:
            flag = 1
            flag = check_duplicate(answer, flag)
            if flag == 1:
                f = open(filename, 'a')
                f.write(answer + '\n')
                f.close()