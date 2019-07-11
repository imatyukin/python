#!/usr/bin/env python3
"""
Given the participants' score sheet for your University Sports Day, you are required to find the runner-up score. You
are given n scores. Store them in a list and find the score of the runner-up.
Input Format
The first line contains n. The second line contains an array A[] of n integers each separated by a space.
Constraints
2 <= n <= 10
-100 <= A[i] <= 100
Output Format
Print the runner-up score.
Sample Input 0
5
2 3 6 6 5
Sample Output 0
5
"""


def runner_up(arr):
    count = 0
    first = second = float('-inf')
    for i in arr:
        if -100 <= i <= 100:
            count += 1
            if i > second:
                if i > first:
                    first, second = i, first
                elif i == first:
                    continue
                else:
                    second = i
        else:
            exit(0)
    return second if count >= 2 else None


if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())

    if 2 <= n <= 10:
        print(runner_up(arr))
