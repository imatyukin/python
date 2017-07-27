#!/usr/bin/env python3

def city_country(city, country):
    capital = city.title() + ", " + country.title()
    return capital

capital = city_country('Santiago', 'Chile')
print(capital)
capital = city_country(country = 'Russia', city = 'Moscow')
print(capital)
capital = city_country('Ho Chi Minh City', 'Vietnam')
print(capital)