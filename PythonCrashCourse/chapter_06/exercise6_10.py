#!/usr/bin/env python3

favorite_numbers = {
'igor': [ 26, 7, 69 ],
'tanya': [ 3, 26 ],
'sonya': [ 2, 4, 2010 ],
'eric': [ 2017 ],
'eduard': [ 74 ],
}

for name, numbers in favorite_numbers.items():
    print(name.title() + "'s favorite numbers are:")
    for number in numbers:
        print("\t" + str(number))
    print("")