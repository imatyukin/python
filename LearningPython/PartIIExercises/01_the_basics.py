#!/usr/bin/env python3

print(2 ** 16)                                           # 65536
print(2 / 5, 2 / 5.0)                                    # 0.4 0.4
print("spam" + "eggs")                                   # spameggs
S = "ham"
print("eggs " + S)                                       # eggs ham
print(S * 5)                                             # hamhamhamhamham
print(S[:0])                                             # ''
print("green %s and %s" % ("eggs", S))                   # green eggs and ham
print('green {0} and {1}'.format('eggs', S))             # green eggs and ham
print(('x',)[0])                                         # x
print(('x', 'y')[1])                                     # y
L = [1, 2, 3] + [4, 5, 6]
print(L, L[:], L[:0], L[:-2], L[-2:])                    # [1, 2, 3, 4, 5, 6] [1, 2, 3, 4, 5, 6] [] [1, 2, 3, 4] [5, 6]
print(([1, 2, 3] + [4, 5, 6])[2:4])                      # [3, 4]
print([L[2], L[3]])                                      # [3, 4]
L.reverse(); print(L)                                    # [6, 5, 4, 3, 2, 1]
L.sort(); print(L)                                       # [1, 2, 3, 4, 5, 6]
print(L.index(4))                                        # 3
print({'a': 1, 'b': 2}['b'])                             # 2
D = {'x': 1, 'y': 2, 'z': 3}
D['w'] = 0
print(D['x'] + D['w'])                                   # 1
D[(1, 2, 3)] = 4
print(list(D.keys()), list(D.values()), (1, 2, 3) in D)  # ['x', 'y', 'z', 'w', (1, 2, 3)] [1, 2, 3, 0, 4] True
print([[]], ["", [], (), {}, None])                      # [[]] ['', [], (), {}, None]
