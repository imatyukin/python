#!/usr/bin/env python3

class Restaurant():

    def __init__(self, restaurant_name, location):
        self.restaurant_name = restaurant_name
        self.location = location

    def describe_restaurant(self):
        print(self.restaurant_name.title())
        print(self.location.title())

    def open_restaurant(self):
        print("Ресторан " + self.restaurant_name.title() + " открыт:")

restaurant_1 = Restaurant('Eleven Madison Park', 'New York (USA)')
restaurant_2 = Restaurant('Osteria Francescana', 'Modena (Italy)')
restaurant_3 = Restaurant('El Celler de Can Roca', 'Girona (Spain)')

restaurant_1.describe_restaurant()
restaurant_2.describe_restaurant()
restaurant_3.describe_restaurant()