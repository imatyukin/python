#!/usr/bin/env python3
"""
Sample Input
6
1 2 3 4 10 11
Sample Output
31
Explanation
We print the sum of the array's elements: 1 + 2 + 3 + 4 + 10 + 11 = 31
"""


#
# Complete the simpleArraySum function below.
#
def simpleArraySum(ar):
    result = 0
    for i in ar:
        result += i
    return result


if __name__ == '__main__':
    ar_count = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = simpleArraySum(ar)

    print(result)
