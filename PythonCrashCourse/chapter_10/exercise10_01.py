#!/usr/bin/env python3

filename = 'learning_python.txt'

print("Вывод текста с чтением всего файла:\n")
with open(filename) as file_object:
    for line in file_object:
        print(line.rstrip())
print("\n")

print("Вывод текста с перебором строк объекта файла:\n")
with open(filename) as file_object:
    lines = file_object.readlines()
    for line in lines:
        print(line.rstrip())
print("\n")

print("Вывод текста с сохранением строк в списке с последующим выводом списка вне блока with:\n")
with open(filename) as file_object:
    lines = file_object.readlines()
for line in lines:
    print(line.rstrip())
