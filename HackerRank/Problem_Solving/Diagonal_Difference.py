#!/usr/bin/env python3
"""
Sample Input
3
11 2 4
4 5 6
10 8 -12
Sample Output
15
Explanation
The primary diagonal is:
11
   5
     -12
Sum across the primary diagonal: 11 + 5 - 12 = 4
The secondary diagonal is:
     4
   5
10
Sum across the secondary diagonal: 4 + 5 + 10 = 19
Difference: |4 - 19| = 15
Note: |x| is the absolute value of x
"""


# Complete the diagonalDifference function below.
def diagonalDifference(arr):
    sum1 = 0
    sum2 = 0
    leading_diag = [arr[i][i] for i in range(len(arr))]
    counter_diag = [row[-i - 1] for i, row in enumerate(arr)]

    for i in range(len(leading_diag)):
        sum1 += leading_diag[i]
    for i in range(len(counter_diag)):
        sum2 += counter_diag[i]

    result = abs(sum1 - sum2)

    return result


if __name__ == '__main__':
    n = int(input())

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    result = diagonalDifference(arr)

    print(result)
