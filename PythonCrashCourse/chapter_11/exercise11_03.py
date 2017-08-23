#!/usr/bin/env python3
import unittest
from employee import Employee

class TestEmployee(unittest.TestCase):
    """Тестовый сценарий для класса Employee."""

    def setUp(self):
        """
        Создание экземпляра Employee для использования в каждом тестовом методе.
        """
        self.employee1 = Employee('Igor', 'Matyukin', 17240)

    def test_give_default_raise(self):
        """Тест увеличения ежегодного оклада на $5000."""
        self.employee1.give_raise()

    def test_give_custom_raise(self):
        """Тест увеличения ежегодного оклада на другую величину прибавки."""
        self.employee1.give_raise(10000)


unittest.main()
