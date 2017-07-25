#!/usr/bin/env python3

favorite_places = {
    'Roma': ['Igor', 'Tanya'],
    'Paris': ['Igor', 'Henry', 'Tanya'],
    'London': ['Igor'],
    }

uniqueNames = []

for place, names in favorite_places.items():
    for name in names:
        if name not in uniqueNames:
            uniqueNames.append(name)

for uniqueName in uniqueNames:
    print(uniqueName.title() + "'s favorite places are:")
    for place, names in favorite_places.items():
        for name in names:
            if name == uniqueName:
                print("\t" + place)
