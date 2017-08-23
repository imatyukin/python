#!/usr/bin/env python3

class Employee():

    def __init__(self, first_name, last_name, annual_salary):
        """Представление работника."""
        self.first_name = first_name
        self.last_name = last_name
        self.annual_salary = annual_salary
        print("Имя, фамилия и ежегодный оклад")
        print(self.first_name + " " + self.last_name +
              " $" + str(self.annual_salary))

    def give_raise(self, increase_annual_salary=5000):
        """Увеличение ежегодного оклада."""
        if increase_annual_salary == 5000:
            print("Увеличение ежегодного оклада на $5000")
        else:
            print("Увеличение ежегодного оклада на $" + str(increase_annual_salary))
        print(self.first_name + " " + self.last_name +
              " $" + str(self.annual_salary + increase_annual_salary))

