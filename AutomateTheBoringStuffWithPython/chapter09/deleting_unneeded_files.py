#!/usr/bin/env python3
import os


def deleting(folder):
    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if (os.path.getsize(os.path.join(foldername, filename)) >> 20) > 100:
                # os.unlink(os.path.join(foldername, filename))
                print(os.path.join(foldername, filename))


def main():
    folder = '/Users/igor/'
    deleting(folder)


if __name__ == "__main__":
    main()
