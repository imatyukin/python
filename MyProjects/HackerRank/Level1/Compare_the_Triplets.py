#!/usr/bin/env python3
"""
Sample Input
5 6 7
3 6 10
Sample Output
1 1
Explanation
In this example:
a = (a[0], a[1], a[2]) = (5, 6, 7)
b = (b[0], b[1], b[2]) = (3, 6, 10)
Now, let's compare each individual score:
a[0] > b[0], so Alice receives 1 point.
a[1] = b[1[, so nobody receives a point.
a[2] < b[2], so Bob receives 1 point.
Alice's comparison score is 1, and Bob's comparison score is 1. Thus, we return the array [1, 1].
"""


# Complete the compareTriplets function below.
def compareTriplets(a, b):
    result_a = 0
    result_b = 0
    for i in range(len(a)):
        if a[i] > b[i]:
            result_a += 1
        elif a[i] < b[i]:
            result_b += 1
        else:
            continue
    return result_a, result_b


if __name__ == '__main__':
    a = list(map(int, input().rstrip().split()))

    b = list(map(int, input().rstrip().split()))

    result = compareTriplets(a, b)

    print(result)
