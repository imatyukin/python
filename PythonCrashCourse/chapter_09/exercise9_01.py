#!/usr/bin/env python3

class Restaurant():

    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(self.restaurant_name.title())
        print(self.cuisine_type.title())

    def open_restaurant(self):
        print("Ресторан " + self.restaurant_name.title() + " открыт:")

restaurant = Restaurant('White Rabbit', 'Камчатский краб')
print("Московский ресторан " + restaurant.restaurant_name.title() + ".")
print("Морепродукты: ")
print(restaurant.cuisine_type + ", фаланги (Мурманск)")
print(restaurant.cuisine_type + ", целиком (Владивосток)")
restaurant.open_restaurant()
print("вс/пн/вт/ср 12:00 - 00:00")
print("чт/пт/сб 12:00 - 02:00")