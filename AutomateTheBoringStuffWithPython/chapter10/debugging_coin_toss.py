#!/usr/bin/env python3
import random


def compare():
    guess = input()

    if guess == 'heads':
        guess = 1
    elif guess == 'tails':
        guess = 0

    return guess


def main():
    guess = ''

    while guess not in (0, 1):
        print('Guess the coin toss! Enter heads or tails:')
        guess = compare()

    toss = random.randint(0, 1) # 0 is tails, 1 is heads

    if toss == guess:
        print('You got it!')
    else:
        print('Nope! Guess again!')
        guess = compare()
        while guess not in (0, 1):
            print('Enter heads or tails:')
            guess = compare()
        toss = random.randint(0, 1)
        if toss == guess:
            print('You got it!')
        else:
            print('Nope. You are really bad at this game.')


if __name__ == "__main__":
    main()
