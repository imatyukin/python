#!/usr/bin/env python3

import sys
sys.path.append('/Users/igor/Documents/workspace/python3/Head First Python/')
import nester

cast = ['Palin', 'Cleese', 'Idle', 'Jones', 'Gilliam', 'Chapman']
print(cast)

nester.print_lol(cast)

from nester import print_lol

print_lol(cast)