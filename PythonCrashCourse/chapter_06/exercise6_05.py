#!/usr/bin/env python3

rivers = {
    'amazon': 'brasil',
    'nile': 'egypt',
    'mississippi': 'usa',
    }

for river, country in rivers.items():
    if river == 'mississippi':
        print("The " + river.title() + " runs through " + country.upper() + ".")
    else:
        print("The " + river.title() + " runs through " + country.title() + ".")

print("\nThe following rivers have been mentioned:")

for river in set(rivers.keys()):
    print(river.title())

print("\nThe following countries have been mentioned:")

for country in set(rivers.values()):
    if country == 'usa':
        print(country.upper())
    else:
        print(country.title())

