#!/usr/bin/env python3
import os
import re
import shutil
import subprocess


def main():
    dir = '/Users/igor/PycharmProjects/python/AutomateTheBoringStuffWithPython/chapter09'
    seq = re.compile(r'^(spam)(\d+)(.txt)')

    subprocess.call(dir + '/insert_gaps.py')

    lst = []
    for file in os.listdir(dir):
        try:
            num = seq.search(file).group(2)
            lst.append((int(num.lstrip('0')), file, len(num)))
        except:
            continue

    lst = sorted(lst)
    for index in range(len(lst)):
        padding = lst[index][2]
        num = str(int(index) + 1)
        padded_num = num.rjust(padding, '0')
        src = os.path.join(dir, lst[index][1])
        dst = os.path.join(dir, seq.sub(r'\g<1>%s\g<3>' % padded_num, lst[index][1]))
        shutil.move(src, dst)


if __name__ == "__main__":
    main()
