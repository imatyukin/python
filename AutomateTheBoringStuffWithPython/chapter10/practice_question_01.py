#!/usr/bin/env python3


def spam(spam):
   assert (not isinstance(spam, int)), "The variable spam is an integer"
   assert (spam > 10), "The variable spam is less than 10"

   return spam


def main():
    print(spam(10.1))
    print(spam(11))
    print(spam(9.0))


if __name__ == "__main__":
    main()
