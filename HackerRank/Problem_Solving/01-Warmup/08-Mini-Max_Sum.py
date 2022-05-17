#!/usr/bin/env python3
"""
Sample Input
1 2 3 4 5
Sample Output
10 14
Explanation
Our initial numbers are 1, 2, 3, 4, and 5. We can calculate the following sums using four of the five integers:
If we sum everything except 1, our sum is 2 + 3 + 4 + 5 = 14.
If we sum everything except 2, our sum is 1 + 3 + 4 + 5 = 13.
If we sum everything except 3, our sum is 1 + 2 + 4 + 5 = 12.
If we sum everything except 4, our sum is 1 + 2 + 3 + 5 = 11.
If we sum everything except 5, our sum is 1 + 2 + 3 + 4 = 10.
"""


# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    min = max = 0
    arr.sort()

    for i in range(0, len(arr)-1):
        min += arr[i]
    for i in range(1, len(arr)):
        max += arr[i]

    return print(min, max)


if __name__ == '__main__':
    arr = list(map(int, input().rstrip().split()))

    miniMaxSum(arr)
