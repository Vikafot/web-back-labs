from flask import Flask, render_template, request, make_response, redirect, url_for, abort
import datetime

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5



app = Flask(__name__)

app.secret_key = 'секретный ключ'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


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
    # === ЛОГИРОВАНИЕ ===
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url

    log_entry = f"{access_time}, пользователь {client_ip} зашёл на адрес: {requested_url}"
    if not hasattr(app, 'error_log'):
        app.error_log = []
    app.error_log.append(log_entry)
    if len(app.error_log) > 20:
        app.error_log.pop(0)

    # === ОТОБРАЖЕНИЕ СТРАНИЦЫ С КАРТИНКОЙ ===
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