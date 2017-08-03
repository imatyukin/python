#!/usr/bin/env python3
from user import User

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