#!/usr/bin/env python3
# 1. Modify the print_unicode.py program so that the user can enter several
#    separate words on the command line, and print rows only where the
#    Unicode character name contains all the words the user has specified.
#    This means that we can type commands like this:
#
#    print_unicode_ans.py greek symbol
#
#    One way of doing this is to replace the word variable (which held 0, None,
#    or a string), with a words list. Don't forget to update the usage information
#    as well as the code. The changes involve adding less than ten lines
#    of code, and changing less than ten more. A solution is provided in file
#    print_unicode_ans.py. (Windows and cross-platform users should modify
#    print_unicode_uni.py; a solution is provided in print_unicode_uni_ans.py.)

import sys
import unicodedata


def print_unicode_table(words):
    print("decimal   hex   chr  {0:^40}".format("name"))
    print("-------  -----  ---  {0:-<40}".format(""))

    code = ord(" ")
    end = min(0xD800, sys.maxunicode) # Stop at surrogate pairs

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")
        # Short Circuiting
        if words is None or all(word in name.lower() for word in words):    # Using all()
            print("{0:7}  {0:5X}  {0:^3c}  {1}".format(
                code, name.title()))
        code += 1


words = None
if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("usage: {0} [string]".format(sys.argv[0]))
        words = 0
    else:
        words = []
        for arg in sys.argv[1:]:
            words.append(arg.lower())
if words != 0:
    print_unicode_table(words)
