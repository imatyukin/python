#!/usr/bin/env python3

def count_word(filename):
    wordCounter = {}
    try:
        with open(filename) as f_obj:
            for line in f_obj:
                word_list = line.replace(',','').replace('\'','').replace('.','').lower().split()
                for word in word_list:
                    if word == 'the':
                        if word not in wordCounter:
                            wordCounter[word] = 1
                        else:
                            wordCounter[word] = wordCounter[word] + 1
        print('\nFile: ' + filename + '\n')
        print('{:15}{:5}'.format('Word', 'Count'))
        print('-' * 20)

        for (word,occurance) in wordCounter.items():
            print('{:15}{:5}'.format(word,occurance) + '\n')
    except FileNotFoundError:
        pass

files = ['alice.txt', 'siddhartha.txt', 'moby_dick.txt', 'little_women.txt']
for filename in files:
    count_word(filename)