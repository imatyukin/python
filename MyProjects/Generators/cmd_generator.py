#!/usr/bin/env python3
import sys
import re

with open(sys.argv[1]) as ifd:
    for line in ifd:
        column = line.split()
        if len(column) > 1:
            if column[1] == 'up' and column[2] == 'up' and re.search(r'ae0\b', column[5]):
                print("show interfaces", column[0], "| match error")