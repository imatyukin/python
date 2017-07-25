#!/usr/bin/env python3

guests = ['Nikola Tesla', 'Albert Einstein', 'Sir Issac Newton', 'Louis Pasteur', 'Marie Curie', \
          'Thomas Alva Edison', 'Michael Faraday', 'Galileo', 'Archimedes', 'Aristotle']

message = ", please be our guest for dinner."

print("Список гостей: " + ', '.join(guests))
print("")
print(guests[-4] + " прийти не сможет.")

for i, guest in enumerate(guests):
    if guest == "Michael Faraday":
        guests.pop(i)
        guests.insert(i, "Mikhail Lomonosov")

print("Новый приглашённый " + guests[-4] + ".")
print("")
print("Новый список гостей: " + ', '.join(guests))
print("")

for i in range(0, 10):
    print(guests[i] + message)