#!/usr/bin/env python3


def comparison(eggs, bacon):
    assert (eggs.lower() != bacon.lower()), "The strings are the same (case insensitive)"

    return "The strings are not the same (case insensitive)"


def main():
    eggs = 'hello'
    bacon = 'goodbye'
    print(comparison(eggs, bacon))
    eggs = 'goodbye'
    bacon = 'GOODbye'
    print(comparison(eggs, bacon))
    eggs = 'hello'
    bacon = 'hello'
    print(comparison(eggs, bacon))


if __name__ == "__main__":
    main()