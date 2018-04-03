#!/usr/bin/env python3
import re


def main():
    password = input("Enter password: ")
    result = strong_password_detection(password)
    if result is True:
        print("The password is strong")
    else:
        print("The password isn't strong")


def strong_password_detection(password):
    length_regex = re.compile(r'.{8,}')
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'[0-9]')

    return (length_regex.search(password) is not None
            and uppercase_regex.search(password) is not None
            and lowercase_regex.search(password) is not None
            and digit_regex.search(password) is not None)


if __name__ == "__main__":
    main()
