from flask import Flask, render_template, request, make_response, redirect, url_for, abort
import datetime

from lab1 import lab1
from lab2 import lab2

app = Flask(__name__)

app.register_blueprint(lab1)
app.register_blueprint(lab2)

@app.route('/')
@app.route('/index')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>HГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>HГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
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
    user_agent = request.headers.get('User-Agent', 'Неизвестно')

    log_entry = f"{access_time}, пользователь {client_ip} зашёл на адрес: {requested_url}"
    if not hasattr(app, 'error_log'):
        app.error_log = []
    app.error_log.append(log_entry)
    if len(app.error_log) > 20:
        app.error_log.pop(0)

    return f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="UTF-8"><title>Страница не найдена</title></head>
    <body>
        <h1>404 - Страница не найдена</h1>
        <p>IP: {client_ip}, время: {access_time}, URL: {requested_url}</p>
        <a href="/">На главную</a>
        <h3>Журнал (последние 20):</h3>
        <pre>{'<br>'.join(reversed(app.error_log))}</pre>
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
