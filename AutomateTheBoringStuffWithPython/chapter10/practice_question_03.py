#!/usr/bin/env python3
# Q: 3. Write an assert statement that always triggers an AssertionError.


class Always:
    pass


def assert_error(arg=None):
    assert (not Always()), "An assert statement always triggers an AssertionError"


def main():
    print(assert_error())


if __name__ == "__main__":
    main()
