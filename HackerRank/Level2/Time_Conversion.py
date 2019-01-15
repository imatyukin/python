#!/usr/bin/env python3
"""
Sample Input
07:05:45PM
Sample Output
19:05:45
"""


#
# Complete the timeConversion function below.
#
def timeConversion(s):
    from datetime import datetime

    return datetime.strptime(s, "%I:%M:%S%p").strftime("%H:%M:%S")


if __name__ == '__main__':
    s = input()

    result = timeConversion(s)

    print(result)
