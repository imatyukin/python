#!/usr/bin/env python3
import make_car

car = make_car.make_car('subaru', 'outback', color ='blue', tow_package = True)
print(car)

from make_car import make_car

car = make_car('subaru', 'outback', color ='blue', tow_package = True)
print(car)

from make_car import make_car as def_mk

car = def_mk('subaru', 'outback', color ='blue', tow_package = True)
print(car)

import make_car as mk

car = mk.make_car('subaru', 'outback', color ='blue', tow_package = True)
print(car)

from make_car import *

car = make_car('subaru', 'outback', color ='blue', tow_package = True)
print(car)
