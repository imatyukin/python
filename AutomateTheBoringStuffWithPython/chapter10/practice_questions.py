#!/usr/bin/env python3


def spam(spam):
    # Q: 1. Write an assert statement that triggers an AssertionError if the variable spam is an integer less than 10.
   assert (not isinstance(spam, int)), "The variable spam is an integer"
   assert (spam > 10), "The variable spam is less than 10"

   return spam


def comparison(eggs, bacon):
    # Q: 2. Write an assert statement that triggers an AssertionError if the variables eggs and bacon contain strings
    # that are the same as each other, even if their cases are different (that is, 'hello' and 'hello' are considered
    # the same, and 'goodbye' and 'GOODbye' are also considered the same).
    assert (eggs.lower() != bacon.lower()), "The strings are the same (case insensitive)"

    return "The strings are not the same (case insensitive)"


class Always:
    pass


def assert_error(arg=None):
    # Q: 3. Write an assert statement that always triggers an AssertionError.
    assert (not Always()), "An assert statement always triggers an AssertionError"


def main():
    # Q1
    print(spam(10.1))
    print(spam(11))
    print(spam(9.0))

    # Q2
    eggs = 'hello'
    bacon = 'goodbye'
    print(comparison(eggs, bacon))
    eggs = 'goodbye'
    bacon = 'GOODbye'
    print(comparison(eggs, bacon))
    eggs = 'hello'
    bacon = 'hello'
    print(comparison(eggs, bacon))

    # Q3
    print(assert_error())


if __name__ == "__main__":
    main()
