#!/usr/bin/env python3

name = "Head First Python"

def what_happens_here():
    
    print(name)
    global name
    name = name + " is a great book!"
    print(name)
    
what_happens_here()
print(name)