#!/usr/bin/env python3
import re


def main():
    string_one = input("Enter the first string: ")
    string_two = input("Enter the second string: ")
    string_new = regex_strip(string_one, string_two)
    print(string_new)


def regex_strip(arg1, arg2=None):
    if arg2 is not None:
        remove_regex = re.compile(arg2)
        string = remove_regex.sub("", arg1)

    striped_string = re.sub("^\s+|\s+$", "", string)

    return striped_string


if __name__ == "__main__":
    main()
