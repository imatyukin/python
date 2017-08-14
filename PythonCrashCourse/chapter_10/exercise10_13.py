#!/usr/bin/env python3
import json

def get_stored_username():
    """Get stored username if available."""
    filename = 'username.json'
    try:
        with open(filename) as f_obj:
            username = json.load(f_obj)
    except FileNotFoundError:
        return None
    else:
        return username

def get_new_username():
    """Prompt for a new username."""
    username = input("\nWhat is your name? ")
    filename = 'username.json'
    with open(filename, 'w') as f_obj:
        json.dump(username, f_obj)
    return username

def greet_user():
    """Greet the user by name."""
    username = get_stored_username()
    if username:
        print("Is your name " + username + "?\n")
        check = input("Press 'yes' or 'no': ")
        if check == 'yes':
            print("\nWelcome back, " + username + "!")
        elif check == 'no':
            username = get_new_username()
            print("\nWe'll remember you when you come back, " + username + "!")
        else:
            print("Wrong input. Try again.\n")
            greet_user()
    else:
        username = get_new_username()
        print("\nWe'll remember you when you come back, " + username + "!")

greet_user()