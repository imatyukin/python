#!/usr/bin/env python3
import os


def main():
    for i in range(1, 4, 2):
        touch('/Users/igor/PycharmProjects/python/AutomateTheBoringStuffWithPython/chapter09/', i)


def touch(path, i):
    with open(path + "spam00{}.txt".format(i), 'a'):
        os.utime(path, None)


if __name__ == "__main__":
    main()
