#!/usr/bin/env python3

'''Глава 9. Распутываем Всемирную паутину'''

'''1. Если вы еще не установили Flask, сделайте это сейчас.
Это также установит werkzeug, jinja2 и, возможно, другие пакеты.'''

# pip3 install flask

print('\n================================ RESTART ================================\n')

'''2. Создайте скелет сайта с помощью веб-сервера Flask. 
Убедитесь, что сервер начинает свою работу по адресу Localhost на стандартном порте 5000. 
Если ваш компьютер уже использует порт 5000 для чего-то еще, воспользуйтесь другим портом.'''

'''from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)'''

print('\n================================ RESTART ================================\n')

'''3. Добавьте функцию home() для обработки запросов к домашней странице. Пусть она возвращает строку It's alive!.'''

'''from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "It's alive!"

if __name__ == "__main__":
    app.run(debug=True)'''

print('\n================================ RESTART ================================\n')

'''4. Создайте шаблон для jinja2, который называется home1.html и содержит следующий контент:
<html>
<head>
<title>It's alive!</title>
<body>
I'm of course referring to {{thing}}, which is {{height}} feet tall and {{color}}.
</body>
</html>'''

print('\n================================ RESTART ================================\n')

'''5. Модифицируйте функцию home() вашего сервера, чтобы она использовала шаблон home1.html. 
Передайте ей три параметра для команды GET: thing, height и color.'''

'''Перейдите в своем клиенте по следующему адресу:
http://localhost:5000/?thing=Octothorpe&height=7&color=green'''

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    thing = request.args.get('thing')
    height = request.args.get('height')
    color = request.args.get('color')
    return render_template('home1.html', thing=thing, height=height, color=color)

if __name__ == "__main__":
    app.run(debug=True)

