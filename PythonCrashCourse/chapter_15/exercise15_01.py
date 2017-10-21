#!/usr/bin/env python3
import matplotlib.pyplot as plt

input_values = list(range(1, 5000))
cubes = [x**3 for x in input_values]

plt.scatter(input_values, cubes, s=40)

# Назначение заголовка диаграммы и меток осей.
plt.title("Cube Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Cube of Value", fontsize=14)

# Назначение диапазона для каждой оси.
plt.tick_params(axis='both', labelsize=14)

plt.show()