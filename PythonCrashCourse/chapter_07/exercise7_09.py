#!/usr/bin/env python3

sandwich_orders = ['Пастрами', 'Чорипан', 'Катсу сандо', 'Гавайский тост', 'Крок-месье', 'Францезина',
                   'Пастрами', 'Леберкезе', 'Запеканка', 'Вада пав', 'Кубинский', 'Бан ми', 'Пастрами']
finished_sandwiches = []

print(sandwich_orders)
print("")

while sandwich_orders:
    if 'Пастрами' in sandwich_orders:
        sandwich_orders.remove('Пастрами')
    else:
        sandwich = sandwich_orders.pop()
        print("Я сделал твой " + sandwich + " сендвич")
        finished_sandwiches.append(sandwich)

print("\nВсе изготовленные сэндвичи:")
for sandwich in finished_sandwiches:
    print(sandwich.title())

print("")
print("Пастрами больше нет:")

print(finished_sandwiches)
