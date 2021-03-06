#!/usr/bin/env python3
# Write an interactive program that maintains lists of strings in files.
#
# When the program is run it should create a list of all the files in the current
# directory that have the .lst extension. Use os.listdir(".") to get all the files
# and filter out those that don't have the .lst extension. If there are no matching
# files the program should prompt the user to enter a filename-adding the .lst
# extension if the user doesn't enter it. If there are one or more .lst files they
# should be printed as a numbered list starting from 1. The user should be asked
# to enter the number of the file they want to load, or 0, in which case they should
# be asked to give a filename for a new file.
#
# If an existing file was specified its items should be read. If the file is empty, or
# if a new file was specified, the program should show a message, "no items are
# in the list".
#
# If there are no items, two options should be offered: "Add" and "Quit". Once
# the list has one or more items, the list should be shown with each item numbered
# from 1, and the options offered should be "Add", "Delete", "Save" (unless
# already saved), and "Quit". If the user chooses "Quit" and there are unsaved
# changes they should be given the chance to save. Here is a transcript of a session
# with the program (with most blank lines removed, and without the "List
# Keeper" title shown above the list each time):
#
#    Choose filename: movies
#
#    -- no items are in the list --
#    [A]dd [Q]uit [a]: a
#    Add item: Love Actually
#
#    1: Love Actually
#    [A]dd [D]elete [S]ave [Q]uit [a]: a
#    Add item: About a Boy
#
#    1: About a Boy
#    2: Love Actually
#    [A]dd [D]elete [S]ave [Q]uit [a]:
#    Add item: Alien
#
#    1: About a Boy
#    2: Alien
#    3: Love Actually
#    [A]dd [D]elete [S]ave [Q]uit [a]: k
#    ERROR: invalid choice--enter one of 'AaDdSsQq'
#    Press Enter to continue...
#    [A]dd [D]elete [S]ave [Q]uit [a]: d
#    Delete item number (or 0 to cancel): 2
#
#    1: About a Boy
#    2: Love Actually
#    [A]dd [D]elete [S]ave [Q]uit [a]: s
#    Saved 2 items to movies.lst
#    Press Enter to continue...
#
#    1: About a Boy
#    2: Love Actually
#    [A]dd [D]elete [Q]uit [a]:
#    Add item: Four Weddings and a Funeral
#
#    1: About a Boy
#    2: Four Weddings and a Funeral
#    3: Love Actually
#    [A]dd [D]elete [S]ave [Q]uit [a]: q
#    Save unsaved changes (y/n) [y]:
#    Saved 3 items to movies.lst
#
# Keep the main() function fairly small (less than 30 lines) and use it to provide
# the program's main loop. Write a function to get the new or existing filename
# (and in the latter case to load the items), and a function to present the options
# and get the user's choice of option. Also write functions to add an item,
# delete an item, print a list (of either items or filenames), load the list, and
# save the list. Either copy the get_string() and get_integer() functions from
# make_html_skeleton.py, or write your own versions.
#
# When printing the list or the filenames, print the item numbers using a field
# width of 1 if there are less than ten items, of 2 if there are less than 100 items,
# and of 3 otherwise.
#
# Keep the items in case-insensitive alphabetical order, and keep track of
# whether the list is "dirty" (has unsaved changes). Offer the "Save" option only
# if the list is dirty and ask the user whether they want to save unsaved changes
# when they quit only if the list is dirty. Adding or deleting an item will make
# the list dirty; saving the list will make it clean again.
#
# A model solution is provided in listkeeper.py; it is less than 200 lines of code.

import os


# Функция создания нового файла.
def create_file(elements):
    f = input("Choose filename: ")
    # Добавляет к файлу расширение .lst, если пользователь не сделал этого.
    if not f.endswith(".lst"):
        f = f + ".lst"
    open(f, 'a').close()
    show_message(elements, f)


# Функция чтения содержимого выбранного пользователем файла.
def read_file(elements, f):
    if os.path.exists(f) and os.path.getsize(f) > 0:
        with open(f) as fin:
            # Чтение содержимого файла.
            print(fin.read())
    else:
        # Если файл пуст или указано имя нового файла.
        show_message(elements, f)


# Функция вывода сообщения и первоначального меню.
def show_message(elements, f):
    print("\n-- no items are in the list --")
    item = input("[A]dd [Q]uit [a]: ")
    if item == "" or item == "A" or item == "a":
        add_elements(elements, f)
    elif item == "Q" or item == "q":
        quit_program(elements, f)
    else:
        print("ERROR: invalid choice--enter one of 'AaQq'")
        input("Press Enter to continue...")
        show_message(elements, f)


# Функция добавления элемента.
def add_elements(elements, f):
    item = input("Add item: ")
    elements.append(item+"\n")
    sort_elements(elements, f)


# Функция сортировки элементов в списке в алфавитном порядке.
def sort_elements(elements, f):
    print()
    # Ширина поля для вывода номеров строк.
    width = 1 if len(elements) < 10 else 2 if len(elements) < 100 else 3
    for i, line in enumerate(sorted(elements)):
        if width == 1:
            print('{:1d}: {}'.format(i + 1, line.rstrip()))
        elif width == 2:
            print('{:2d}: {}'.format(i + 1, line.rstrip()))
        else:
            print('{:3d}: {}'.format(i + 1, line.rstrip()))
    show_menu(elements, f)


# Функция предлагающая варианты действий.
def show_menu(elements, f):
    item = input("[A]dd [D]elete [S]ave [Q]uit [a]: ")
    if item == "" or item == "A" or item == "a":
        add_elements(elements, f)
    elif item == "D" or item == "d":
        del_element(elements, f)
    elif item == "S" or item == "s":
        save_elements(elements, f)
    elif item == "Q" or item == "q":
        quit_program(elements, f)
    else:
        print("ERROR: invalid choice--enter one of 'AaDdSsQq'")
        input("Press Enter to continue...")
        show_menu(elements, f)


# Функция удаления элемента из нумерованного списка.
def del_element(elements, f):
    item = int(input("Delete item number (or 0 to cancel): "))
    if item == 0:
        sort_elements(elements, f)
    else:
        for i, line in enumerate(sorted(elements)):
            if item-1 == i:
                elements.remove(line)
    sort_elements(elements, f)


# Сохранение внесённых элементов списка в файл.
def save_elements(elements, f):
    count = 1
    with open(f, 'a') as fa:
        for i, line in enumerate(sorted(elements)):
            fa.write(line.rstrip())
            fa.write("\n")
            count += i
    print("Saved "+str(count)+" items to "+str(f))
    input("Press Enter to continue...")
    show_menu_without_save(elements, f)


# Функция предлагающая варианты действий (без действия сохранить).
def show_menu_without_save(elements, f):
    print()
    for i, line in enumerate(sorted(elements)):
        print('{}: {}'.format(i + 1, line.rstrip()))
    item = input("[A]dd [D]elete [Q]uit [a]: ")
    if item == "" or item == "A" or item == "a":
        add_elements(elements, f)
    elif item == "D" or item == "d":
        del_element(elements, f)
    elif item == "Q" or item == "q":
        quit_program(elements, f)
    else:
        print("ERROR: invalid choice--enter one of 'AaDdQq'")
        input("Press Enter to continue...")
        show_menu_without_save(elements, f)


# Функция выхода из программы.
def quit_program(elements, f):
    item = input("Save unsaved changes (y/n) [y]: ")
    if item == "" or item == "Y" or item == "y":
        count = 0
        with open(f, 'w') as fa:
            for i, line in enumerate(sorted(elements)):
                fa.write(line.rstrip())
                fa.write("\n")
                count += i
        print("Saved " + str(count) + " items to " + str(f))
        exit(0)
    elif item == "N" or item == "n":
        exit(0)
    else:
        print("ERROR: invalid choice--enter one of 'YyNn'")
        input("Press Enter to continue...")
        quit_program(elements, f)


# Вывод имён .lst файлов в виде списка пронумерованных строк, начиная с 1.
def show_lst(files):
    count = 1
    for i, filename in enumerate(files):
        print('{0:3d}. {1}'.format(count, filename))
        count += 1


def main():
    # Интерактивная программа обслуживания списков строк в файлах.
    print("List Keeper")
    print()
    # Список всех файлов с расширением .lst в текущем каталоге.
    files = []
    # Список добавленных элементов
    elements = []
    # os.listdir(".") получает список всех файлов.
    for f in [f for f in os.listdir("exercises") if os.path.isfile(f)]:
        # Фильтр файлов, которые имеют расширение .lst
        if f.endswith(".lst"):
            files.append(f)
    if not files:
        # В случае отсутствия .lst файлов программа создаёт новый файл.
        create_file(elements)
    else:
        # В случае, если были найдены один или более файлов .lst.
        show_lst(files)
        number = int(input("\nEnter the number of the file or 0: "))
        # Если пользователь ввёл 0, программа просит у пользователся ввести имя нового файла.
        if number == 0:
            create_file(elements)
        else:
            # При вводе номера желаемого файла, программа читает его содержимое.
            try:
                file = files[number - 1]
                read_file(elements, file)
            # Если пользователь указал несуществующий номер файла.
            except IndexError:
                print("ERROR: file not exist")


if __name__ == "__main__":
    main()
