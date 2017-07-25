#!/usr/bin/env python3

current_users = ['root', 'admin', 'master', 'igor', 'tanya']

new_users = ['root', 'admin', 'IGOR', 'kamchatka', 'last_hero']

for user in new_users:
    if user.lower() in current_users:
        print("Вы должны выбрать новое имя.")
    else:
        print("Имя доступно.")
