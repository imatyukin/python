#!/usr/bin/env python3
import matplotlib.pyplot as plt

from my_random_walk import RandomWalk

# Новые блуждания строятся до тех пор, пока программа остается активной.
while True:
    # Построение случайного блуждания и нанесение точек на диаграмму.
    rw = RandomWalk(5000)
    rw.fill_walk()

    # Назначение размера области просмотра.
    plt.figure(dpi=128, figsize=(10, 6))

    # Вывод точек и отображение диаграммы.
    point_numbers = list(range(rw.num_points))
    plt.plot(rw.x_values, rw.y_values, linewidth=1, zorder=1)

    # Выделение первой и последней точек.
    plt.scatter(0, 0, c='green', edgecolors='none', s=75, zorder=2)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors='none',
                s=75, zorder=2)

    # Удаление осей.
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("Make another walk? (y/n): ")
    if keep_running == 'n':
        break