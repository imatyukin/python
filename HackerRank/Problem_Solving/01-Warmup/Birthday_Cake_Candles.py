#!/usr/bin/env python3
"""
Sample Input
4
3 2 1 3
Sample Output
2
Explanation
We have one candle of height 1, one candle of height 2, and two candles of height 3. Your niece only blows out the
tallest candles, meaning the candles where height = 3. Because there are 2 such candles, we print 2 on a new line.
"""


# Complete the birthdayCakeCandles function below.
def birthdayCakeCandles(ar):
    candles = 0
    ar.sort()
    for i in range(len(ar)):
        if ar[i] == ar[-1]:
            candles += 1

    return candles


if __name__ == '__main__':
    ar_count = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = birthdayCakeCandles(ar)

    print(result)
