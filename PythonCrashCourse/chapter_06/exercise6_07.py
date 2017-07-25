#!/usr/bin/env python3

igor = {
    'first_name': 'Igor',
    'last_name': 'Matyukin',
    'age': 37,
    'city': 'Saint Petersburg'
    }

albert = {
    'first_name': 'Albert',
    'last_name': 'Einstein',
    'age': 76,
    'city': 'Princeton'
    }
    
diego = {
    'first_name': 'Diego',
    'last_name': 'Maradona',
    'age': 56,
    'city': 'Buenos Aires'
    }

people = [igor, albert, diego]

for username in people:
    full_name = username['first_name'] + " " + username['last_name']
    age = username['age']
    location = username['city']
    print("Full name: " + full_name.title())
    print("Age: " + str(age))
    print("Location: " + location.title())
    print("")
