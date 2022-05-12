#!/usr/bin/env python3

D = {9: 'nine', 8: 'eight', 7: 'seven', 6: 'six', 5: 'five', 4: 'four', 3: 'three', 2: 'two', 1: 'one'}
print(D)
for key in sorted(D):
    print(key, ':', D[key])
