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
python3 manage.py makemigrations learning_logs
python3 manage.py migrate

# Административный сайт Django
# Создание суперпользователя
# python3 manage.py createsuperuser
# login/password: ll_admin/ll_admin

# Интерактивная оболочка Django
# python3 manage.py shell

# Создание нового приложения users
# python manage.py startapp users
# login/password: ll_user/SuperLL_User123

# Сброс содержимого базы данных
# python3 manage.py flush

# Установка django-bootstrap3
# pip3 install django-bootstrap3

# Установка пакетов, упрощающих работу проектов Django на реальных серверах
# Помогает Django взаимодействовать с базой данных, используемой Heroku
# pip3 install dj-database-url
# Позволяют Django правильно управлять статическими файлами
# pip3 install dj-static
# pip3 install static3
# Сервер, способный предоставлять доступ к приложениям в реальной среде
# pip3 install gunicorn

# Создание списка пакетов с файлом requirements.txt
# pip3 freeze > requirements.txt

# Локальное использование сервера gunicorn
# heroku local

# Закрепление состояния проекта
# Инициализирует пустой репозиторий в каталоге
# git init
# Добавляет все файлы (кроме игнорируемых) в репозиторий
# git add .
# Флаг -a приказывает Git включить все измененные файлы в закрепленное состояние,
# флаг -m приказывает Git сохранить сообщение в журнале
# git commit -am "Ready for deployment to heroku."
# Сообщает статус
# git status

# Отправка проекта
# Вход на сервер Heroku в терминальном сеансе
# heroku login
# Построение пустого проекта Heroku
# heroku create
# Приказывает Git отправить главную ветвь проекта в репозиторий
# git push heroku master

# Проверка, что серверный процесс был запущен правильно
# heroku ps

# Открыть приложение в браузере
# heroku open

# Подготовка базы данных в Heroku
# heroku run python manage.py migrate

# Выполнение команд в терминальном сеансе Bash при подключении к серверу Heroku
# heroku run bash
# Создание суперпользователя в Heroku
# python manage.py createsuperuser

# Создание удобного URL-адреса на Heroku
# heroku apps:rename learning-log
