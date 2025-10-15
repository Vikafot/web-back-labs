from flask import Blueprint, render_template, redirect, url_for, request, abort
import datetime

lab1 = Blueprint('lab1', __name__)

count = 0
error_log = []


@lab1.route('/lab1/web')
def web():
    return """<!doctype html> \
    <html> \
        <body> \
            <h1>web-сервер на flask</h1> \
            <a href="/lab1/author">author</a> \
        </body> \
    </html>"""


@lab1.route('/lab1/author')
def author():
    name = "Фот Виктория Владимировна"
    group = "ФБИ-33"
    faculty = "ФБ"
    return f"""<!doctype html>
          <html>
             <body>
              <p>Студент: {name}</p>
              <p>Группа: {group}</p>
              <p>Факультет: {faculty}</p>
              <a href="/lab1/web">web</a>
              </body>
            </html>"""


@lab1.route('/lab1')
def lab1_index():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">На главную</a>
        <h2>Список роутов лабораторной работы 1</h2>
        <ul>
            <li><a href="/lab1/web">Главная страница лабораторной</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Страница с изображением кота</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/lab1/info">Перенаправление на автора</a></li>
            <li><a href="/lab1/error">Генерация ошибки 500</a></li>
            <li><a href="/lab1/400">Тест кода 400</a></li>
            <li><a href="/lab1/401">Тест кода 401</a></li>
            <li><a href="/lab1/402">Тест кода 402</a></li>
            <li><a href="/lab1/403">Тест кода 403</a></li>
            <li><a href="/lab1/405">Тест кода 405</a></li>
            <li><a href="/lab1/418">Тест кода 418</a></li>
        </ul>
    </body>
    </html>
    '''


@lab1.route('/lab1/400')
def bad_request():
    return '<h1>400 - Плохой запрос</h1><p>Сервер не может обработать запрос</p>', 400

@lab1.route('/lab1/401')
def unauthorized():
    return '<h1>401 - Не авторизован</h1><p>Требуется аутентификация</p>', 401

@lab1.route('/lab1/402')
def payment_required():
    return '<h1>402 - Требуется оплата</h1><p>Необходима оплата для доступа</p>', 402

@lab1.route('/lab1/403')
def forbidden():
    return '<h1>403 - Запрещено</h1><p>Доступ к ресурсу запрещен</p>', 403

@lab1.route('/lab1/405')
def method_not_allowed():
    return '<h1>405 - Метод не разрешен</h1><p>HTTP метод не поддерживается</p>', 405

@lab1.route('/lab1/418')
def teapot():
    return '<h1>418 - Я чайник</h1><p>Сервер отказывается варить кофе</p>', 418


@lab1.route('/lab1/error')
def generate_error():
    1 / 0


@lab1.route('/lab1/image')
def image():
    image_path = url_for('static', filename='lab1/кот.jpg')
    css_path = url_for('static', filename='lab1/lab1.css')
    html_content = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Кот</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>Кот</h1>
        <img src="{image_path}" alt="Кот">
        <br>
        <a href="/lab1">На главную</a>
    </body>
    </html>
    '''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-Header': 'MyValue'
    }


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.now()
    url = request.url
    client_ip = request.remote_addr
    server_name = request.host
    return f'''
<!doctype html>
<html>
    <head><meta charset="UTF-8"><title>Счетчик посещений</title></head>
    <body>
        <h1>Счетчик посещений</h1>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <hr>
        <p>Дата и время: {time}</p>
        <p>Запрошенный адрес: {url}</p>
        <p>Ваш IP-адрес: {client_ip}</p>
        <p>Имя сервера: {server_name}</p>
        <a href="/lab1/counter/clear">Очистить счетчик</a><br>
    </body>
</html>
'''


@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')