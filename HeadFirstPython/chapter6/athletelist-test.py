#!/usr/bin/env python3

from athletelist import AthleteList
from athletelist import get_coach_data

james = get_coach_data('james2.txt')
julie = get_coach_data('julie2.txt')
mikey = get_coach_data('mikey2.txt')
sarah = get_coach_data('sarah2.txt')

print(james.name + "'s fastest times are: " + str(james.top3()))
print(julie.name + "'s fastest times are: " + str(julie.top3()))
print(mikey.name + "'s fastest times are: " + str(mikey.top3()))
print(sarah.name + "'s fastest times are: " + str(sarah.top3()))

vera = AthleteList('Vera Vi')
print(vera.top3())
vera.append('1.31')
vera.extend(['2.22', "1-21", '2:22'])
print(vera.top3())
print(vera.name + "'s fastest times are: " + str(vera.top3()))