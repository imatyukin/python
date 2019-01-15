#!/usr/bin/env python3
"""
Sample Input
6
Sample Output
     #
    ##
   ###
  ####
 #####
######
Explanation
The staircase is right-aligned, composed of # symbols and spaces, and has a height and width of n = 6.
"""


# Complete the staircase function below.
def staircase(n):
    for stairs in range(1, n + 1):
        print(' ' * (n - stairs) + '#' * stairs)


if __name__ == '__main__':
    n = int(input())

    staircase(n)
