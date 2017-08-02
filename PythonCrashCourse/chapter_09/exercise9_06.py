#!/usr/bin/env python3

class Restaurant():

    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        print(self.restaurant_name.title())
        print(self.cuisine_type.title())

    def open_restaurant(self):
        print("Ресторан " + self.restaurant_name.title() + " открыт:")

    def set_number_served(self, number_served):
        self.number_served = number_served

    def increment_number_served(self, number_increment):
        self.number_served += number_increment

class IceCreamStand(Restaurant):

    def __init__(self, restaurant_name, cuisine_type, flavors):
        super().__init__(restaurant_name, cuisine_type)
        self.flavors = flavors

    def ice_cream_varieties(self):
        ice_cream = "Список сортов мороженного: " + self.flavors + "."
        print(ice_cream)

ice_cream = IceCreamStand('Киоск с мороженным', 'Мороженное', 'ванильное, шоколадное, крем-брюле, с шоколадом, со вкусом ягод и фруктов, кофейное')
ice_cream.ice_cream_varieties()


