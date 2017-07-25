#!/usr/bin/env python3

mushroom = 'Мухомор'
print(mushroom == 'Мухомор')
print(mushroom == 'Боровик')

print(mushroom.lower() == 'Мухомор')
print(mushroom)

hour = 20
minute = 53
print(hour >= 21 and minute >= 21)
hour = 22
print(hour >= 21 and minute >= 21)

hour = 20
minute = 55
print(hour >= 21 or minute >= 21)
hour = 18
print(hour >= 21 or minute >= 21)

mushrooms = ['Боровик', 'Трюфель', 'Мухомор', 'Бледная поганка', 'Шампиньон', 'Веселка', 'Навозник',
             'Шиитаке (древесный японский гриб)', 'Звездовик или земляная звезда', 'Плазмодий']

print('Мухомор' in mushrooms)
print('Мухомор красный' in mushrooms)
