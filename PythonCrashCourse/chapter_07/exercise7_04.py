#!/usr/bin/env python3

prompt = "Введите дополнения для пиццы:"
prompt += "\n(введите 'quit' для завершения)\n"

pizza = []
topping = ""
while topping != 'quit':
    topping = input(prompt)
    if topping != 'quit':
        print("Дополнение " + topping + " включено в заказ.")
        pizza.append(topping)
toppings = ''
for i in range(0, len(pizza)):
    toppings = toppings + pizza[i] + ' '
print("Ваш пицца со следующей начинкой: " + toppings)
