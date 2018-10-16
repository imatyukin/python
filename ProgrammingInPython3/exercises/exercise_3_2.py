#!/usr/bin/env python3
# 2. Modify the uniquewords2.py program so that it outputs the words in frequency
#    of occurrence order rather than in alphabetical order. You'll need
#    to iterate over the dictionary's items and create a tiny two-line function
#    to extract each item's value and pass this function as sorted()'s key function.
#    Also, the call to print() will need to be changed appropriately. This
#    isn't difficult, but it is slightly subtle. A solution is provided in uniquewords_ans.py.

import collections
import string
import sys


words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    with open(filename) as file:
        for line in file:
            for word in line.lower().split():
                word = word.strip(strip)
                if len(word) > 2:
                    words[word] += 1

for k, v in sorted(words.items(), key=lambda kv: kv[1], reverse=True):
    print("'{0}' occurs {1} times".format(k, v))
