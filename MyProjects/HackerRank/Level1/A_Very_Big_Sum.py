#!/usr/bin/env python3
"""
Sample Input
5
1000000001 1000000002 1000000003 1000000004 1000000005
Output
5000000015
"""


# Complete the aVeryBigSum function below.
def aVeryBigSum(ar):
    sum = 0
    for i in ar:
        sum += i
    return sum

if __name__ == '__main__':
    ar_count = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = aVeryBigSum(ar)

    print(result)
