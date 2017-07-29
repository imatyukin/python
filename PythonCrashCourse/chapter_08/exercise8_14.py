#!/usr/bin/env python3

def make_car(manufacturer, model_name, **car_info):
    car = {}
    car['manufacturer'] = manufacturer
    car['model_name'] = model_name
    for key, value in car_info.items():
        car[key] = value
    return car

subaru = make_car('subaru', 'outback', color ='blue', tow_package = True)
hyundai = make_car('hyundai', 'elantra', color ='blazing yellow', equipment = 'Comfort + Style + High-Tech (AD) 2,0 AT 17PY')
print(subaru)
print(hyundai)