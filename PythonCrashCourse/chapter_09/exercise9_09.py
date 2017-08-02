#!/usr/bin/env python3
from car import Car

class Battery():
    """Простая модель аккумулятора электромобиля."""

    def __init__(self, battery_size=60):
        """Инициализирует атрибуты аккумулятора."""
        self.battery_size = battery_size

    def describe_battery(self):
        """Выводит информацию о мощности аккумулятора."""
        print("This car has a " + str(self.battery_size) + "-kWh battery.")

    def get_range(self):
        """Выводит приблизительный запас хода для аккумулятора."""
        if self.battery_size == 60:
            range = 140
        elif self.battery_size == 85:
            range = 185

        message = "This car can go approximately " + str(range)
        message += " miles on a full charge."
        print(message)

    def upgrade_battery(self):
        """Проверяет размер аккумулятора и устанавливает мощность равной 85, если она имеет другое значение."""
        if self.battery_size != 85:
            self.battery_size = 85

class ElectricCar(Car):
    """Представляет аспекты машины, специфические для электромобилей."""

    def __init__(self, manufacturer, model, year):
        """
        Инициализирует атрибуты класса-родителя.
        Затем инициализирует атрибуты, специфические для электромобиля.
        """
        super().__init__(manufacturer, model, year)
        self.battery = Battery()

my_tesla = ElectricCar('tesla', 'roadster', 2015)
my_tesla.battery.get_range()
my_tesla.battery.upgrade_battery()
my_tesla.battery.get_range()
