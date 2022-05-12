#!/usr/bin/env python3
import os
import re


def main():
    dir = '/Users/igor/PycharmProjects/python/AutomateTheBoringStuffWithPython/chapter09/'
    pattern = re.compile(r'^(spam)(\d+)(.txt)')

    purge(dir, pattern)

    for i in range(1, 4, 2):
        touch(dir, i)


def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


def touch(dir, i):
    with open(dir + "spam00{}.txt".format(i), 'a'):
        os.utime(dir, None)


if __name__ == "__main__":
    main()
