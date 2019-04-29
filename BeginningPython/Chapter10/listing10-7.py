# fortune.py

import fileinput, random

fortunes = list(fileinput.input())
print(random.choice(fortunes))
