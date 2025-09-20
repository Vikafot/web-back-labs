from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route('/lab1/web')
def web():
    return """<!doctype html> \
    <html> \
        <body> \
            <h1>web-сервер на flask</h1> \
            <a href="/author">author</a> \
        </body> \
    </html>"""

@app.route('/lab1/author')
def author():
    name = "Фот Виктория Владимировна"
    group = "ФБИ-33"
    faculty = "ФБ"
    
    return """<!doctype html>
          <html>
             <body>
              <p>Студент: """ + name + """</p>
              <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/web">web</a>
               </body>
            </html>"""

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
            </ul>
        </nav>
        
        <footer>
            <p>Фот Виктория Владимировна, ФБИ-33, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    '''

@app.route('/lab1')
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
        
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
        Относится к категории так называемых микрофреймворков — минималистичных каркасов 
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/">На главную</a>
        
        <h2>Список роутов лабораторной работы 1</h2>
        <ul>
            <li><a href="/lab1/web">Главная страница лабораторной</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Страница с изображением кота</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/lab1/info">Перенаправление на автора</a></li>
            <li><a href="/lab1/error">Генерация ошибки 500</a></li>
            <li><a href="/lab1/400">Тест кода 400 - Плохой запрос</a></li>
            <li><a href="/lab1/401">Тест кода 401 - Не авторизован</a></li>
            <li><a href="/lab1/402">Тест кода 402 - Требуется оплата</a></li>
            <li><a href="/lab1/403">Тест кода 403 - Запрощено</a></li>
            <li><a href="/lab1/405">Тест кода 405 - Метод не разрешен</a></li>
            <li><a href="/lab1/418">Тест кода 418 - Я чайник</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/lab1/400')
def bad_request():
    return '<h1>400 - Плохой запрос</h1><p>Сервер не может обработать запрос</p>', 400

@app.route('/lab1/401')
def unauthorized():
    return '<h1>401 - Не авторизован</h1><p>Требуется аутентификация</p>', 401

@app.route('/lab1/402')
def payment_required():
    return '<h1>402 - Требуется оплата</h1><p>Необходима оплата для доступа</p>', 402

@app.route('/lab1/403')
def forbidden():
    return '<h1>403 - Запрещено</h1><p>Доступ к ресурсу запрещен</p>', 403

@app.route('/lab1/405')
def method_not_allowed():
    return '<h1>405 - Метод не разрешен</h1><p>HTTP метод не поддерживается</p>', 405

@app.route('/lab1/418')
def teapot():
    return '<h1>418 - Я чайник</h1><p>Сервер отказывается варить кофе</p>', 418

error_log = []


@app.errorhandler(404)
def not_found(error):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')

    log_entry = f"{access_time}, пользователь {client_ip} зашёл на адрес: {requested_url}"
    error_log.append(log_entry)

    if len(error_log) > 20:
        error_log.pop(0)
    
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
                background-color: #f8f9fa;
            }}
            .error {{
                color: #d9534f;
                font-size: 2.5em;
                margin-bottom: 20px;
            }}
            .info {{
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin: 20px auto;
                max-width: 600px;
                text-align: left;
            }}
            .journal {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin: 20px auto;
                max-width: 800px;
                text-align: left;
                font-family: monospace;
                font-size: 0.9em;
            }}
            .journal-entry {{
                margin: 5px 0;
                padding: 5px;
                border-bottom: 1px solid #ddd;
            }}
            .journal-entry:last-child {{
                border-bottom: none;
            }}
            a {{
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            img {{
                max-width: 300px;
                margin: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <h1 class="error">404 - Страница не найдена</h1>
        
        <div class="info">
            <p>Запрашиваемая страница не существует.</p>
            <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
            <p><strong>Время доступа:</strong> {access_time}</p>
            <p><strong>Запрошенный URL:</strong> {requested_url}</p>
            <p><strong>Браузер:</strong> {user_agent}</p>
        </div>

        <img src="{url_for('static', filename='ошибка.jpg')}" alt="Ошибка 404">
        <br>
        
        <a href="/">Вернуться на главную</a>
        
        <div class="journal">
            <h3>Журнал обращений (последние 20 записей):</h3>
            {"".join([f'<div class="journal-entry">{entry}</div>' for entry in error_log[::-1]])}
        </div>
    </body>
    </html>
    ''', 404


@app.route('/lab1/error')
def generate_error():
    result = 1 / 0
    return "Эта строка никогда не будет выполнена"

@app.errorhandler(500)
def internal_error(error):
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>Произошла непредвиденная ошибка на сервере.</p>
        <a href="/">Вернуться на главную</a>
    </body>
    </html>
    ''', 500

@app.route('/lab1/image')
def image():
    image_path = url_for('static', filename='кот.jpg')
    css_path = url_for('static', filename='lab1.css')
    
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
        <a href="/lab1/web">На главную</a>
    </body>
    </html>
    '''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-Header': 'MyValue',
        'X-Another-Header': 'Test'
    }


count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    

    time = datetime.datetime.now() 
    url = request.url
    client_ip = request.remote_addr
    server_name = request.host  
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Счетчик посещений</title>
    </head>
    <body>
        <h1>Счетчик посещений</h1>
        <p>Сколько раз вы сюда заходили: ''' + str(count) + '''</p>
        <hr>
        <p>Дата и время: ''' + str(time) + '''</p>
        <p>Запрошенный адрес: ''' + str(url) + '''</p>
        <p>Ваш IP-адрес: ''' + str(client_ip) + '''</p>
        <p>Имя сервера: ''' + str(server_name) + '''</p>
 
        <a href="/lab1/counter/clear">Очистить счетчик</a><br>
    </body>
</html>
'''

@app.route('/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route("/lole")
def lole():
    return """<!doctype html>
    <html>
       <body>
          <h1>Создано успешно</h1>
          <div><i>что-то создано...</i></div>
        </body>
    </html>""", 201


@app.route("/lol")
def lol():
    return """<!doctype html>
          <html>
             <body>
               <h1>web-сервер на flask</h1>
               </body>
            </html>""", 200, {
                'X-Server': 'sample',
                'Content-Type': 'text/plain; charset=utf-8'
            }