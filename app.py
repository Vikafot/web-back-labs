from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html> \
    <html> \
        <body> \
            <h1>web-сервер на flask</h1> \
            <a href="/author">author</a> \
        </body> \
    </html>"""

@app.route("/author")
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

@app.route('/counter')
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



@app.route("/info")
def info():
    return redirect("/author")

@app.route("/lole")
def lole():
    return """<!doctype html>
    <html>
       <body>
          <h1>Создано успешно</h1>
          <div><i>что-то создано...</i></div>
        </body>
    </html>""", 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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