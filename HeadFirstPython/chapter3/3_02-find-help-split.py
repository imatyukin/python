#!/usr/bin/env python3

data = open('sketch.txt')

each_line = "I tell you, there's no such thing as a flying circus."
print(each_line.find(':'))

each_line = "I tell you: there's no such thing as a flying circus."
print(each_line.find(':'))

help(each_line.split)

for each_line in data:
    if not each_line.find(':') == -1:
        (role, line_spoken) = each_line.split(':', 1)
        print(role, end='')
        print(' said: ', end='')
        print(line_spoken, end='')
    else:
        print(each_line, end='')
    
data.close()