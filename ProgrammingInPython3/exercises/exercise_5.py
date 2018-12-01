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
import time
import argparse


def file_processing(files, dirs, top, modified, order, sizes):
    keys_lines = []
    mtimestring = ""
    for name in files:
        if modified:
            mtime = os.stat(name).st_mtime
            mtimestring = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(mtime))
        size = ""
        if sizes:
            size = "{0:>15n} ".format(os.stat(name).st_size)
        if os.path.islink(name):
            name += " -> " + os.path.realpath(name)
        if order in {"m", "modified1"}:
            orderkey = mtimestring
        elif order in {"s", "size"}:
            orderkey = size
        else:
            orderkey = name
        keys_lines.append((orderkey, "{mtimestring}{size}{name}".format(**locals())))
    size = "" if not sizes else " " * 15
    modified = "" if not modified else " " * 20
    for name in sorted(dirs):
        keys_lines.append((name, mtimestring + size + name + "/"))
    for key, line in sorted(keys_lines):
        print(line)


def filter_walk(top, hidden=False, modified=False, order='name', recursive=False, sizes=False):
    dirs_count = 0
    files_count = 0
    files = []
    dirs = []
    for entry in top:
        if recursive is False:
            if hidden is False:
                if os.path.isfile(entry):
                    if not entry.startswith("."):
                        files.append(entry)
                        files_count += 1
                elif os.path.isdir(entry):
                    for name in os.listdir(entry):
                        if not name.startswith("."):
                            fullname = os.path.join(entry, name)
                            if os.path.isfile(fullname):
                                files.append(fullname)
                                files_count += 1
                            elif os.path.isdir(fullname):
                                dirs.append(fullname)
                                dirs_count +=1
                else:
                    print(f'Файл {entry} не найден.')
            else:
                if os.path.isfile(entry):
                    files.append(entry)
                    files_count += 1
                else:
                    for item in os.listdir(entry):
                        if os.path.isfile(item):
                            files.append(item)
                            files_count += 1
                        else:
                            dirs.append(item)
                            dirs_count += 1
            file_processing(files, dirs, top, modified, order, sizes)
            print(f'\n{files_count} files, {dirs_count} directories')
        else:
            for path, dirs, files in os.walk(top):
                if hidden is False:
                    dirs[:] = [dir for dir in dirs if not dir.startswith(".")]
                real_path = os.path.abspath(os.path.realpath(path))
                print('Directory: {:s}'.format(real_path))
                dirs_count += 1
                for file in files:
                    fstat = os.stat(os.path.join(path, file))
                    fsize = fstat.st_size
                    mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(fstat.st_mtime))
                    print('{:18s}\t{:10d}\t{:15.15s}'.format(mtime, fsize, file))
                    files_count += 1
            print('\n{} files, {} directories'.format(files_count, dirs_count))


def parser_arguments():
    usage = """%(prog)s [options] [path1 [path2 [... pathN]]]

The paths are optional; if not given . is used."""

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-H", "--hidden", dest="hidden",
                        action="store_true",
                        help="show hidden files [default: off]")
    parser.add_argument("-m", "--modified", dest="modified",
                        action="store_true",
                        help="show last modified date/time [default: off]")
    orderlist = ["name", "n", "modified", "m", "size", "s"]
    parser.add_argument("-o", "--order", dest="order",
                        choices=orderlist,
                        help=("order by ({0}) [default: %(default)s]".format(
                            ", ".join(["'" + x + "'" for x in orderlist]))))
    parser.add_argument("-r", "--recursive", dest="recursive",
                        action="store_true",
                        help="recurse into subdirectories [default: off]")
    parser.add_argument("-s", "--sizes", dest="sizes",
                        action="store_true",
                        help="show sizes [default: off]")
    parser.set_defaults(order=orderlist[0])
    args, top = parser.parse_known_args()
    if not top:
        top = ["."]
    return args, top


def main():
    opts, top = parser_arguments()
    filter_walk(top=top, hidden=opts.hidden, modified=opts.modified, order=opts.order,
                recursive=opts.recursive, sizes=opts.sizes)


if __name__ == "__main__":
    main()
