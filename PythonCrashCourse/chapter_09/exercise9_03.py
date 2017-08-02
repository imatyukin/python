#!/usr/bin/env python3

class User():

    def __init__(self, first_name, last_name, user_id, group_name):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.group_name = group_name

    def describe_user(self):
        print(self.first_name.title() + " " + self.last_name.title() + ": "
              + str(self.user_id) + ", " + self.group_name)

    def greet_user(self):
        print("Hello " + self.first_name.title() + "!")

user1 = User('root', '', 0, 'wheel')
user2 = User('Igor', 'Matyukin', 1, 'wheel')

user1.describe_user()
user2.describe_user()
user1.greet_user()
user2.greet_user()