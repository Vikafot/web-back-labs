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

@app.errorhandler(404)
def not_found(error):
    image_path = url_for('static', filename='ошибка.jpg')
    
    return f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Страница не найдена</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
            .error {{ color: #d9534f; }}
        </style>
    </head>
    <body>
        <h1 class="error">404 - Страница не найдена</h1>
        <p>Запрашиваемая страница не существует.</p>
        <img src="{image_path}" alt="Ошибка 404" width="500">
        <br>
        <a href="/">Вернуться на главную</a>
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
    
    return f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Кот</title>
        <link rel="stylesheet" href="{css_path}"> 
    </head>
    <body>
        <h1>Кот</h1>
        <img src="{image_path}" alt="Дуб">
        <br>
        <a href="/lab1/web">На главную</a>
    </body>
    </html>
    '''


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