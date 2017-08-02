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

class Privileges():

    def __init__(self):
        self.privileges = '«разрешено добавлять сообщения», «разрешено удалять пользователей», «разрешено банить пользователей»'

    def show_privileges(self):
        privileges = "Привилегии администратора: " + self.privileges + "."
        print(privileges)

class Admin(User):

    def __init__(self, first_name, last_name, user_id, group_name):
        super().__init__(first_name, last_name, user_id, group_name)
        self.privileges = Privileges()

admin = Admin('root', '', '0', 'wheel')
admin.privileges.show_privileges()
