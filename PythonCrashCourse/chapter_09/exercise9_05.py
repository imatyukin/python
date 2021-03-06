#!/usr/bin/env python3

class User():

    def __init__(self, first_name, last_name, user_id, group_name):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.group_name = group_name
        self.login_attempts = 0

    def describe_user(self):
        print(self.first_name.title() + " " + self.last_name.title() + ": "
              + str(self.user_id) + ", " + self.group_name)

    def greet_user(self):
        print("Hello " + self.first_name.title() + "!")

    def increment_login_attempts(self, login_attempts_increment):
        self.login_attempts =+ login_attempts_increment

    def reset_login_attempts(self):
        self.login_attempts = 0

user = User('Igor', 'Matyukin', 1, 'wheel')
user.increment_login_attempts(3)
print(user.login_attempts)
user.reset_login_attempts()
print(user.login_attempts)

