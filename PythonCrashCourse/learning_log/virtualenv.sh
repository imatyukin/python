#!/usr/bin/env sh

# Установка virtualenv
# pip3 install --user virtualenv

# Создание виртуальной среды
# python3 -m venv ll_env

# Активизация виртуальной среды
source ll_env/bin/activate

# Завершить использование виртуальной среды
# deactivate

# Установка Django
# pip3 install Django

# Создание проекта в Django
# django-admin.py startproject learning_log .

# Создание базы данных
# python3 manage.py migrate

# Просмотр проекта
python3 manage.py runserver

# Начало работы над приложением
# python3 manage.py startapp learning_logs

# Активизация моделей
# python3 manage.py makemigrations learning_logs
# python3 manage.py migrate

# Административный сайт Django
# Создание суперпользователя
# python3 manage.py createsuperuser