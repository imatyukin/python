#!/usr/bin/env python3


class Always:
    pass


def assert_error(arg=None):
    assert (not Always()), "An assert statement always triggers an AssertionError"


def main():
    print(assert_error())


if __name__ == "__main__":
    main()
