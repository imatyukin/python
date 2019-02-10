#!/usr/bin/env python3

print("\U0001F60A")
print("This is a cat: \N{Cat}")

x = bytearray(b"Hello!")
x[1] = ord(b"u")
print(x)
