#!/usr/bin/env python3

guests = ['Nikolay Lobachevsky', 'Nikola Tesla', 'Albert Einstein', 'Sir Issac Newton', 'Louis Pasteur', \
          'Dmitri Mendeleev', 'Marie Curie', 'Thomas Alva Edison', 'Mikhail Lomonosov', 'Galileo', \
          'Archimedes', 'Aristotle', 'Ivan Pavlov']

message = ", более раннее приглашение остаётся в силе."

print("Места хватит только для двух гостей: " + guests[1] + " и " + guests[2] + ".")
print("")

ind2pop = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for guest in sorted(ind2pop, reverse=True):
    print(guests[guest] + ", мы сожалеем об отмене приглашения.")
    guests.pop(guest)

print("")
print(guests)
print("")
for i in range(0, 2):
    print(guests[i] + message)

del guests[:]

print("")
print("This is the list 'guests':", guests)