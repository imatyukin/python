#!/usr/bin/env python3
import matplotlib.pyplot as plt

input_values = list(range(1, 5000))
cubes = [x**3 for x in input_values]

# plt.scatter(input_values, cubes, c='red', edgecolor='none', s=40)
# plt.scatter(input_values, cubes, c=(0, 0, 0.8), edgecolor='none', s=40)
plt.scatter(input_values, cubes, c=cubes, cmap=plt.cm.Blues, edgecolor='none', s=40)

# Назначение заголовка диаграммы и меток осей.
plt.title("Cube Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Cube of Value", fontsize=14)

# Назначение диапазона для каждой оси.
# plt.tick_params(axis='both', labelsize=14)
plt.axis([0, 5100, 0, 130000000000])

plt.show()