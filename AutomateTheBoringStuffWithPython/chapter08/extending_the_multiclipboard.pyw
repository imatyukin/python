#!/usr/bin/env python3
# extending_the_multiclipboard.pyw - Saves and loads pieces of text to the clipboard.
# Usage: python3 extending_the_multiclipboard.pyw save <keyword> - Saves clipboard to keyword.
#        python3 extending_the_multiclipboard.pyw <keyword> - Loads keyword to clipboard.
#        python3 extending_the_multiclipboard.pyw list - Loads all keywords to clipboard.
#        python3 extending_the_multiclipboard.pyw delete <keyword> - Delete a keyword from the shelf.
#        python3 extending_the_multiclipboard.pyw delete - Delete all keywords.

import shelve
import pyperclip
import sys


def main():
    with shelve.open('extending_the_multiclipboard') as mcbShelf:

        # Save clipboard content.
        if len(sys.argv) == 3:
            if sys.argv[1].lower() == 'save':
                mcbShelf[sys.argv[2]] = pyperclip.paste()
            elif sys.argv[1].lower() == 'delete':
                del mcbShelf[sys.argv[2]]
        elif len(sys.argv) == 2:
            # List keywords and load content.
            if sys.argv[1].lower() == 'list':
                pyperclip.copy(str(list(mcbShelf.keys())))
            elif sys.argv[1] in mcbShelf:
                pyperclip.copy(mcbShelf[sys.argv[1]])
            elif sys.argv[1].lower() == 'delete':
                for key in mcbShelf.keys():
                    del mcbShelf[key]


if __name__ == "__main__":
    main()
