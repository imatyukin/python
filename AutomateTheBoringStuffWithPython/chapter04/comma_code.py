#!/usr/bin/env python3


def main():
    spam = ['apples', 'bananas', 'tofu', 'cats']
    newString(spam)


def newString(arg):
    print(', '.join(arg[:-1]) + ', and ' + str(arg[-1]))


if __name__ == "__main__":
    main()