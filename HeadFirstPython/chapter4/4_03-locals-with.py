#!/usr/bin/env python3

try:
    data = open('missing.txt')
    print(data.readline(), end='')
except IOError as err:
    print('File error: ' + str(err))
finally:
    if 'data' in locals():
        data.close()

print('\n================================ RESTART ================================\n')

try:
    data = open('its.txt', "w")
    print("It's...", file=data)
except IOError as err:
    print('File error: ' + str(err))
finally:
    if 'data' in locals():
        data.close()
        
try:
    with open('its.txt', "w") as data:
        print("It's...", file=data)
except IOError as err:
    print('File error: ' + str(err))

print('\n================================ RESTART ================================\n')

""" try:
    man_file = open('man_data.txt', 'w')
    other_file = open('other_data.txt', 'w')
    
    print(man, file=man_file)
    print(other, file=other_file)
except IOError as err:
    print('File error: ' + str(err))
finally:
    if 'man_file' in locals():
        man_file.close()
    if 'other_file' in locals():
        other_file.close() """

man = []
other = []

"""try:
    with open('man_data.txt', 'w') as man_file:
        print (man, file=man_file)
    with open('other_data.txt', 'w') as other_file:
        print(other, file=other_file)
except IOError as err:
    print('File error: ' + str(err)) """

try:
    with open('man_data.txt', 'w') as man_file, open('other_data.txt', 'w') as other_file:
        print(man, file=man_file)
        print(other, file=other_file)
except IOError as err:
    print('File error: ' + str(err))