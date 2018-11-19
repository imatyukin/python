#!/usr/bin/env python3
# Write a program to show directory listings, rather like the dir command in
# Windows or ls in Unix. The benefit of creating our own listing program is
# that we can build in the defaults we prefer and can use the same program on
# all platforms without having to remember the differences between dir and ls.
# Create a program that supports the following interface:
#
#     Usage: ls.py [options] [path1 [path2 [... pathN]]]
#     The paths are optional; if not given . is used.
#     Options:
#     -h, --help      show this help message and exit
#     -H, --hidden    show hidden files [default: off]
#     -m, --modified  show last modified date/time [default: off]
#     -o ORDER, --order=ORDER
#                     order by ('name', 'n', 'modified', 'm', 'size', 's') [default: name]
#     -r, --recursive recurse into subdirectories [default: off]
#     -s, --sizes     show sizes [default: off]
#
# (The output has been modified slightly to fit the book’s page.)
#
# Here is an example of output on a small directory using the command line
# ls.py -ms -os misc/:
#
#     2008-02-11 14:17:03    12,184 misc/abstract.pdf
#     2008-02-05 14:22:38   109,788 misc/klmqtintro.lyx
#     2007-12-13 12:01:14 1,359,950 misc/tracking.pdf
#                                   misc/phonelog/
#     3 files, 1 directory
#
# We used option grouping in the command line (optparse handles this automatically
# for us), but the same could have been achieved using separate options, for
# example, ls.py -m -s -os misc/, or by even more grouping, ls.py -msos misc/, or
# by using long options, ls.py --modified --sizes --order=size misc/, or any combination
# of these. Note that we define a “hidden” file or directory as one whose
# name begins with a dot (.).
#
# The exercise is quite challenging. You will need to read the optparse documentation
# to see how to provide options that set a True value, and how to offer a
# fixed list of choices. If the user sets the recursive option you will need to process
# the files (but not the directories) using os.walk(); otherwise, you will have
# to use os.listdir() and process both files and directories yourself.
#
# One rather tricky aspect is avoiding hidden directories when recursing. They
# can be cut out of os.walk()’s dirs list—and therefore skipped by os.walk()—by
# modifying that list. But be careful not to assign to the dirs variable itself, since
# that won’t change the list it refers to but will simply (and uselessly) replace it;
# the approach used in the model solution is to assign to a slice of the whole list,
# that is, dirs[:] = [dir for dir in dirs if not dir.startswith(".")].
#
# The best way to get grouping characters in the file sizes is to import the locale
# module, call locale.setlocale() to get the user’s default locale, and use the n
# format character. Overall, ls.py is about 130 lines split over four functions.

import os
import sys
import argparse


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = MyParser()

parser = argparse.ArgumentParser(description="ls.py")
parser.add_argument('-h, --help',
                    help="show this help message and exit")
parser.add_argument('-H, --hidden',
                    help="show hidden files [default: off]")
parser.add_argument('-m, --modified',
                    help="show last modified date/time [default: off]")
parser.add_argument('-o ORDER, --order=ORDER',
                    help="order by ('name', 'n', 'modified', 'm', 'size', 's') [default: name]")
parser.add_argument('-r, --recursive',
                    help="recurse into subdirectories [default: off]")
parser.add_argument('-s, --sizes',
                    help="show sizes [default: off]")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args=parser.parse_args()

for root, dirs, files in os.walk("."):
    for filename in files:
        print(filename)
