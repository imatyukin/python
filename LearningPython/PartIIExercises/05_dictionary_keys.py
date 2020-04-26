#!/usr/bin/env python3

D = {}
D[1] = 'a'
D[2] = 'b'
print(D)                # {1: 'a', 2: 'b'}
D[(1, 2, 3)] = 'c'
print(D)                # {1: 'a', 2: 'b', (1, 2, 3): 'c'}
