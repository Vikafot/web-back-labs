import os
from os import path
from flask import Flask, render_template, request, make_response, redirect, url_for, abort
import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from flask_login import LoginManager
from db.models import users

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9



app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret_key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


if app.config['DB_TYPE'] == 'postgres':
    db_name = 'ivan_ivanov_orm'
    db_user = 'ivan_ivanov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8, url_prefix='/lab8')
app.register_blueprint(lab9)


@app.route('/')
@app.route('/index')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных работ.</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвёртая лабораторная</a></li>
                <li><a href="/lab5">Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>
                <li><a href="/lab7">Седьмая лабораторная</a></li>
                <li><a href="/lab8">Восьмая лабораторная</a></li>
                <li><a href="/lab9">Девятая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>Фот Виктория Владимировна, ФБИ-33, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    '''

@app.errorhandler(404)
def not_found(error):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url

    log_entry = f"{access_time}, пользователь {client_ip} зашёл на адрес: {requested_url}"
    if not hasattr(app, 'error_log'):
        app.error_log = []
    app.error_log.append(log_entry)
    if len(app.error_log) > 20:
        app.error_log.pop(0)

    image_path = url_for('static', filename='lab1/ошибка.jpg')
    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Страница не найдена</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
        }}
        .error {{
            color: #d9534f;
        }}
        .log {{
            text-align: left;
            margin: 20px auto;
            max-width: 600px;
            font-family: monospace;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1 class="error">404 - Страница не найдена</h1>
    <p>Запрашиваемая страница не существует.</p>
    <img src="{image_path}" alt="Ошибка 404" width="500">
    <br><br>
    <a href="/">Вернуться на главную</a>

    <div class="log">
        <h3>Последние 5 ошибок:</h3>
        {'<br>'.join(reversed(app.error_log[-5:]))}
    </div>
</body>
</html>
''', 404


@app.errorhandler(500)
def internal_error(error):
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="UTF-8"><title>Ошибка сервера</title></head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <a href="/">На главную</a>
    </body>
    </html>
    ''', 500


if __name__ == '__main__':
    app.run(debug=True)