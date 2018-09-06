#!/usr/bin/env python3
# 1. One nice variation of the bigdigits.py program is where instead of
#    printing *s, the relevant digit is printed instead. For example:
#
#        bigdigits_ans.py 719428306
#        77777   1   9999     4     222    888    333     000     666
#            7  11  9   9    44    2   2  8   8  3   3   0   0   6
#           7    1  9   9   4 4    2  2   8   8      3  0     0  6
#          7     1   9999  4  4      2     888     33   0     0  6666
#         7      1      9  444444   2     8   8      3  0     0  6   6
#        7       1      9     4    2      8   8  3   3   0   0   6   6
#        7     111      9     4    22222   888    333     000     666
#
#    Two approaches can be taken. The easiest is to simply change the *s in
#    the lists. But this isn't very versatile and is not the approach you should
#    take. Instead, change the processing code so that rather than adding each
#    digit's row string to the line in one go, you add character by character, and
#    whenever a * is encountered you use the relevant digit.
#
#    This can be done by copying bigdigits.py and changing about five lines.
#    It isn't hard, but it is slightly subtle. A solution is provided as bigdig-
#    its_ans.py.

import sys


Zero = ["  ***  ",
        " *   * ",
        "*     *",
        "*     *",
        "*     *",
        " *   * ",
        "  ***  "]
One = [" * ", "** ", " * ", " * ", " * ", " * ", "***"]
Two = [" *** ", "*   *", "*  * ", "  *  ", " *   ", "*    ", "*****"]
Three = [" *** ", "*   *", "    *", "  ** ", "    *", "*   *", " *** "]
Four = ["   *  ", "  **  ", " * *  ", "*  *  ", "******", "   *  ",
        "   *  "]
Five = ["*****", "*    ", "*    ", " *** ", "    *", "*   *", " *** "]
Six = [" *** ", "*    ", "*    ", "**** ", "*   *", "*   *", " *** "]
Seven = ["*****", "    *", "   * ", "  *  ", " *   ", "*    ", "*    "]
Eight = [" *** ", "*   *", "*   *", " *** ", "*   *", "*   *", " *** "]
Nine = [" ****", "*   *", "*   *", " ****", "    *", "    *", "    *"]

Digits = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]

try:
    digits = sys.argv[1]
    row = 0
    while row < 7:
        line = ""
        column = 0
        while column < len(digits):
            number = int(digits[column])
            digit = Digits[number]
            for item in digit[row]:
                str_number = str(number)
                if item == '*':
                    newrow = digit[row].replace(item, str_number)
            line += newrow + "  "
            column += 1
        print(line)
        row += 1
except IndexError:
    print("usage: bigdigits.py <number>")
except ValueError as err:
    print(err, "in", digits)
