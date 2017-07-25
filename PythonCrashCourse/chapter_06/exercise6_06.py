#!/usr/bin/env python3

persons = ['eric', 'jen', 'sarah', 'edward', 'phil', 'igor']

favorite_languages = {
'jen': 'python',
'sarah': 'c',
'edward': 'ruby',
'phil': 'python',
}

for name in persons:
    if name in favorite_languages.keys():
        print("Привет " + name.title() + ", благодарим за участие в опросе!")
        print("Я вижу, что ваш любимый язык программирования " + favorite_languages[name].title())
    else:
        print(name.title() + ', предлагаем принять участие в опросе "ваш любимый язык программирования".')
