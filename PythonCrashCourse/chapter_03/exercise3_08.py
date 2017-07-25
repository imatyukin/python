#!/usr/bin/env python3

countries = ["United States of America", "Chinese People's Republic", "Australia", "Cuba", "India"]

print("Here is the original list:")
print(countries)

print("\nHere is the sorted list:")
print(sorted(countries))

print("\nHere is the original list again:")
print(countries)

print("\nHere is the sorted list with reverse=True:")
print(sorted(countries, reverse=True))

print("\nHere is the original list again:")
print(countries)

print("\nreverse():")
countries.reverse()
print(countries)

print("\nreverse() again:")
countries.reverse()
print(countries)

print("\nsort():")
countries.sort()
print(countries)

print("\nsort() with reverse=True:")
countries.sort(reverse=True)
print(countries)
