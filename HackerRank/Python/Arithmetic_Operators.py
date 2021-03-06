#!/usr/bin/env python3
"""
Task
Read two integers from STDIN and print three lines where:
The first line contains the sum of the two numbers.
The second line contains the difference of the two numbers (first - second).
The third line contains the product of the two numbers.
Input Format
The first line contains the first integer, a. The second line contains the second integer, b.
Constraints
1 <= a <= 10^10
1 <= b <= 10^10
Output Format
Print the three lines as explained above.
Sample Input 0
3
2
Sample Output 0
5
1
6
"""


def aop(a, b):
    print(a + b)
    print(a - b)
    print(a * b)


if __name__ == '__main__':
    a = int(input())
    b = int(input())

    if (1 <= a <= pow(10,10)) and (1 <= b <= pow(10,10)):
        aop(a, b)
