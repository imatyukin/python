#!/usr/bin/env python3
# 3. In some situations we need to generate test text—for example, to populate
#    a web site design before the real content is available, or to provide test
#    content when developing a report writer. To this end, write a program that
#    generates awful poems (the kind that would make a Vogon blush).
#
#    Create some lists of words, for example, articles (“the”, “a”, etc.), subjects
#    (“cat”, “dog”, “man”, “woman”), verbs (“sang”, “ran”, “jumped”),and adverbs
#    (“loudly”, “quietly”, “well”, “badly”). Then loop five times, and on each
#    iteration use the random.choice() function to pick an article, subject, verb,
#    and adverb. Use random.randint() to choose between two sentence structures:
#    article, subject, verb, and adverb, or just article, subject, and verb,
#    and print the sentence. Here is an example run:
#
#        awfulpoetry1_ans.py
#        another boy laughed badly
#        the woman jumped
#        a boy hoped
#        a horse jumped
#        another man laughed rudely
#
#    You will need to import the random module. The lists can be done in about
#    4–10 lines depending on how many words you put in them, and the loop
#    itself requires less than ten lines, so with some blank lines the whole
#    program can be done in about 20 lines of code. A solution is provided as
#    awfulpoetry1_ans.py.

import random

articles = ["the", "a", "another"]
subjects = ["cat", "dog", "man", "woman", "boy", "horse"]
verbs = ["sang", "ran", "jumped", "laughed", "hoped"]
adverbs = ["loudly", "quietly", "well", "badly", "rudely"]

struct_1 = articles, subjects, verbs, adverbs
struct_2 = articles, subjects, verbs

struct = struct_1, struct_2

for i in range(0, 5):
    sentence = ''
    for j in random.choice(struct):
        word = random.choice(j)
        sentence += ' ' + word
    print(sentence)