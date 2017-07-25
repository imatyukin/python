#!/usr/bin/env python3

cities = {
    'Cанкт-Петербург': {'country': 'Россия', 'population': 5281579, 'fact': 'Город-Герой Ленинград'},
    'Лондон': {'country': 'Великобритания', 'population': 8538689, 'fact': 'Лондонский метрополитен старейший в мире'},
    'Париж': {'country': 'Франция', 'population': 2196936, 'fact': 'Пер-Лашез - кладбище в Париже'},
    }

for name, information in cities.items():
    print("Город " + name)
    country = information['country']
    population = information['population']
    fact = information['fact']
    print("\tСтрана: " + country.title() + ";")
    print("\tЧисленность населения: " + str(population) + " человек;")
    print("\tПримечательный факт: " + fact + ".")
    print("")