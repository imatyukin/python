#!/usr/bin/env python3
import shutil
import os


def selective_copy(folder, new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("Made new directory {}".format(new_folder))

    for foldername, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.pdf') or filename.endswith('.jpg'):
                shutil.copy(os.path.join(foldername, filename), new_folder)
                print("Copy {}".format(os.path.join(foldername, filename)))


def main():
    folder = '/Users/igor/Downloads/'
    new_folder = '/Users/igor/CopyFolder/'
    selective_copy(folder, new_folder)


if __name__ == "__main__":
    main()
