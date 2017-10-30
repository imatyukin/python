#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs

def transliterate(string):

    capital_letters = {u"А": u"A",
                       u"Б": u"B",
                       u"В": u"V",
                       u"Г": u"G",
                       u"Д": u"D",
                       u"Е": u"E",
                       u"З": u"Z",
                       u"И": u"I",
                       u"Й": u"J",
                       u"К": u"K",
                       u"Л": u"L",
                       u"М": u"M",
                       u"Н": u"N",
                       u"О": u"O",
                       u"П": u"P",
                       u"Р": u"R",
                       u"С": u"S",
                       u"Т": u"T",
                       u"У": u"U",
                       u"Ф": u"F",
                       u"Х": u"H",
                       u"Ъ": u"'",
                       u"Ы": u"Y",
                       u"Ь": u"'",
                       u"Э": u"E",}

    capital_letters_transliterated_to_multiple_letters = {u"Ё": u"Yo",
                                                          u"Ж": u"Zh",
                                                          u"Ц": u"Ts",
                                                          u"Ч": u"Ch",
                                                          u"Ш": u"Sh",
                                                          u"Щ": u"Sch",
                                                          u"Ю": u"Yu",
                                                          u"Я": u"Ya",}

    lower_case_letters = {u"а": u"a",
                          u"б": u"b",
                          u"в": u"v",
                          u"г": u"g",
                          u"д": u"d",
                          u"е": u"e",
                          u"ё": u"yo",
                          u"ж": u"zh",
                          u"з": u"z",
                          u"и": u"i",
                          u"й": u"j",
                          u"к": u"k",
                          u"л": u"l",
                          u"м": u"m",
                          u"н": u"n",
                          u"о": u"o",
                          u"п": u"p",
                          u"р": u"r",
                          u"с": u"s",
                          u"т": u"t",
                          u"у": u"u",
                          u"ф": u"f",
                          u"х": u"h",
                          u"ц": u"ts",
                          u"ч": u"ch",
                          u"ш": u"sh",
                          u"щ": u"sch",
                          u"ъ": u"'",
                          u"ы": u"y",
                          u"ь": u"'",
                          u"э": u"e",
                          u"ю": u"yu",
                          u"я": u"ya",}

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in capital_letters_transliterated_to_multiple_letters.items():
        for lowercase_letter, lowercase_letter_translit in lower_case_letters.items():
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.items():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string

if __name__ == "__main__":
    with codecs.open('translit.csv', 'w', 'utf-8') as translit:
        with codecs.open('russian.csv', 'r', 'utf-8') as russian:
            for line in iter(russian.readline, ""):
                translit.write(transliterate(line))