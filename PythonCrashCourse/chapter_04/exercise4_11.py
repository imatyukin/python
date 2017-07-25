#!/usr/bin/env python3

pizzas = ["Lahma Bi Ajeen", "Margherita", "Calzone", "Stromboli", "Marinara", "Neapolitan", "Deep Dish"]
friend_pizzas = pizzas[:]

pizzas.append("California Style")
friend_pizzas.append("New York Style")

print("My favorite pizzas are:")
for pizza in pizzas:
    print(pizza)

print("\nMy friend’s favorite pizzas are:")
for pizza in friend_pizzas:
    print(pizza)

print("\nComparing two lists:")
print([a for a in pizzas+friend_pizzas if (a not in pizzas) or (a not in friend_pizzas)])