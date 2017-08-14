#!/usr/bin/env python3
import json

def get_stored_favorite_number():
    """Get stored favorite_number if available."""
    filename = 'favorite_number.json'
    try:
        with open(filename) as f_obj:
            favor_number = json.load(f_obj)
    except FileNotFoundError:
        return None
    else:
        return favor_number

def get_favorite_number():
    """Prompt for a new favorite number."""
    favor_number = input("Какое ваше любимое число? ")
    filename = 'favorite_number.json'
    with open(filename, 'w') as f_obj:
        json.dump(favor_number, f_obj)
    return favor_number

def favorite_number():
    """Saved favorite number."""
    favor_number = get_stored_favorite_number()
    if favor_number:
        print("Я знаю ваше любимое число! Это " + favor_number + ".")
    else:
        favor_number = get_favorite_number()

favorite_number()