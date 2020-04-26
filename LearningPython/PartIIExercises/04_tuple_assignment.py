#!/usr/bin/env python3

X = 'spam'
Y = 'eggs'
print("X=", X, ", Y=", Y, sep="")
X, Y = Y, X
print("X=", X, ", Y=", Y, sep="")
