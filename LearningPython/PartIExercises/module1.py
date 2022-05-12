#!/usr/bin/env python3


def main():
    print("Hello World!")

    print(2**500)

    L = [1, 2]
    L.append(L)
    print(L)

    try:
        print(1 / 0)
    except ZeroDivisionError:
        print(0)


if __name__ == "__main__":
    main()