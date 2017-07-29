#!/usr/bin/env python3

def make_great(magicians):
    great_magicians = []
    while (magicians):
        magician = "Great " + magicians.pop()
        great_magicians.append(magician)
    for great_magician in great_magicians:
        magicians.insert(0, great_magician)

def show_magicians(magicians):
    for magician in magicians:
        print(magician)

magicians = ['Николя-Филипп Ледрю', 'Алессандро Калиостро', 'Джузеппе Пинетти', 'Джованни Бартоломео Боско',
             'Гарри Гудини', 'Дэвид Вернер', 'Эмиль Теодорович Гиршфельд-Ренард', 'Игорь Кио', 'Ури Геллер',
             'Дэвид Копперфильд', 'Дэвид Блейн']

make_great(magicians)
show_magicians(magicians)