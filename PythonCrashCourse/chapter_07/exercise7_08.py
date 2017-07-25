#!/usr/bin/env python3

sandwich_orders = ['Чорипан', 'Катсу сандо', 'Гавайский тост', 'Крок-месье', 'Францезина',
                   'Леберкезе', 'Запеканка', 'Вада пав', 'Кубинский', 'Бан ми']

finished_sandwiches = []

while sandwich_orders:
    sandwich = sandwich_orders.pop()
    print("Я сделал твой " + sandwich + " сендвич")
    finished_sandwiches.append(sandwich)

print("\nВсе изготовленные сэндвичи:")
for sandwich in finished_sandwiches:
    print(sandwich.title())