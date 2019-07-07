#!/usr/bin/env python3
"""
Task
Given an integer, n, perform the following conditional actions:
If n is odd, print Weird
If n is even and in the inclusive range of 2 to 5, print Not Weird
If n is even and in the inclusive range of 6 to 20, print Weird
If n is even and greater than 20, print Not Weird
Input Format
A single line containing a positive integer, n.
Constraints
1 <= n <= 100
Output Format
Print Weird if the number is weird; otherwise, print Not Weird.
Sample Input 0
3
Sample Output 0
Weird
"""

import math
import os
import random
import re
import sys


def actions(n):
    # is_odd = (value & 1) == 1
    if (n & 1) == 1:
        print("Weird")
    # is_even = (value & 1) == 0
    if (n & 1) == 0 and n in range(2, 6):
        print("Not Weird")
    if (n & 1) == 0 and n in range(6, 21):
        print("Weird")
    if (n & 1) == 0 and n > 20:
        print("Not Weird")


if __name__ == '__main__':
    n = int(input().strip())

    if 1 <= n <= 100:
        actions(n)
    else:
        exit(1)
