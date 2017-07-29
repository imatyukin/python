#!/usr/bin/env python3

def make_car(manufacturer, model_name, **car_info):
    car = {}
    car['manufacturer'] = manufacturer
    car['model_name'] = model_name
    for key, value in car_info.items():
        car[key] = value
    return car