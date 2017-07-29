#!/usr/bin/env python3

def order_sandwich(*toppings):
    print("Описание заказанного сэндвича:")
    print("хлеб; начинка и топпинг: " + ', '.join(toppings) + "; cоус и приправы.\n")

order_sandwich('сыр')
order_sandwich('свежие и жаренные на гриле овощи', 'салаты')
order_sandwich('фалафел', 'тофу', 'темпей')

