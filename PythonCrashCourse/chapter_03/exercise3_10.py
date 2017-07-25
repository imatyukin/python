#!/usr/bin/env python3

mountains = ['Mount Everest', 'K2', 'Kangchenjunga', 'Lhotse', 'Makalu', 'Cho Oyu', 'Dhaulagiri I', 'Manaslu', \
             'Nanga Parbat', 'Annapurna I', 'Gasherbrum I', 'Broad Peak', 'Gasherbrum II', 'Shishapangma', \
             'Gyachung Kang', 'Gasherbrum III', 'Annapurna II', 'Gasherbrum IV', 'Himalchuli', 'Distaghil Sar', \
             'Ngadi Chuli', 'Nuptse']

print(mountains)
print(mountains[0])
print(mountains[0].title())
print(mountains[1])
print(mountains[3])
print(mountains[-1])
message = "List of highest mountains on Earth: " + mountains[0].title() + "."
print(message)
mountains.append('Masherbrum')
print(mountains)
mountains[22] = 'Khunyang Chhish'
print(mountains)
mountains.insert(23, 'Masherbrum')
print(mountains)
del mountains[23]
print(mountains)
popped_mountains = mountains.pop()
print(mountains)
print(popped_mountains)
print("The last popped mountain was " + popped_mountains.title() + ".")
last_popped = mountains.pop(21)
print('The last popped mountain was ' + last_popped.title() + '.')
mountains.remove('Ngadi Chuli')
print(mountains)
mountains.sort()
print(mountains)
mountains.sort(reverse=True)
print(mountains)
mountains = ['Mount Everest', 'K2', 'Kangchenjunga', 'Lhotse', 'Makalu', 'Cho Oyu', 'Dhaulagiri I', 'Manaslu', \
             'Nanga Parbat', 'Annapurna I', 'Gasherbrum I', 'Broad Peak', 'Gasherbrum II', 'Shishapangma', \
             'Gyachung Kang', 'Gasherbrum III', 'Annapurna II', 'Gasherbrum IV', 'Himalchuli', 'Distaghil Sar', \
             'Ngadi Chuli', 'Nuptse']
print(mountains)
print(sorted(mountains))
print(mountains)
mountains.reverse()
print(mountains)
mountains.reverse()
print(mountains)
print(len(mountains))

