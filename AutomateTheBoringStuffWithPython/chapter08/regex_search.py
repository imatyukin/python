#!/usr/bin/env python3
import os
import re


def main():

    pattern = re.compile('^#')
    files = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.txt'):
            files.append(open(filename))

    for file in files:
        for line in file.read().splitlines():
            if re.findall(pattern, line):
                print(line)


if __name__ == '__main__':
    main()
