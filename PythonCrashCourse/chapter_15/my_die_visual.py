#!/usr/bin/env python3
import pygal

from die import Die

# Создание кубика D6.
die = Die()

# Моделирование серии бросков с сохранением результатов в списке.
results = [die.roll() for roll_num in range(1000)]

# Анализ результатов.
frequencies = [results.count(value) for value in range(1, die.num_sides + 1)]

# Визуализация результатов.
hist = pygal.Bar()

hist.title = "Results of rolling one D6 1000 times."
hist.x_labels = [str(x) for x in range(1, die.num_sides + 1)]
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add('D6', frequencies)
hist.render_to_file('die_visual.svg')