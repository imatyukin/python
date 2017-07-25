#!/usr/bin/env python3

guests = ['Nikola Tesla', 'Albert Einstein', 'Sir Issac Newton', 'Louis Pasteur', 'Marie Curie', \
          'Thomas Alva Edison', 'Mikhail Lomonosov', 'Galileo', 'Archimedes', 'Aristotle']

message = ", please be our guest for dinner."

new_guest1 = "Nikolay Lobachevsky"
new_guest2 = "Dmitri Mendeleev"
new_guest3 = "Ivan Pavlov"
print("На обед приглашены ещё трое гостей: " + new_guest1 + ", " + new_guest2 + ", " + new_guest3 + ".")

guests.insert(0, new_guest1)
guests.insert(5, new_guest2)
guests.append(new_guest3)

print("Новый список гостей: " + ', '.join(guests))
print("")

for i in range(0, 13):
    print(guests[i] + message)