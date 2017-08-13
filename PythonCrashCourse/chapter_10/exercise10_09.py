#!/usr/bin/env python3

files = ['cats.txt', 'dogs.txt']

for filename in files:
   try:
       with open(filename) as pets:
           for line in pets:
               line = line.strip()
               if not line:
                   continue
               else:
                   print(line.rstrip())
   except FileNotFoundError:
       pass