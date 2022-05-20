#!/usr/bin/env python3
"""
Sample Input
6
-4 3 -9 0 4 1
Sample Output
0.500000
0.333333
0.166667
Explanation
There are 3 positive numbers, 2 negative numbers, and 1 zero in the array.
The proportions of occurrence are positive: 3/6 = 0.500000, negative: 2/6 = 0.333333 and zeros: 1/6 = 0.166667.
"""


# Complete the plusMinus function below.
def plusMinus(arr):
    pos = neg = zero = 0
    arr_len = len(arr)

    for i in arr:
        if i > 0:
            pos += 1
        elif i < 0:
            neg += 1
        else:
            zero += 1
    pos /= arr_len
    neg /= arr_len
    zero /= arr_len

    return print('{:.6f}\n{:.6f}\n{:.6f}'.format(pos, neg, zero))


if __name__ == '__main__':
    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    plusMinus(arr)
