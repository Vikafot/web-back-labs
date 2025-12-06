from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__,
                 static_folder='static',
                 template_folder='templates')

@lab8.route('/')
def lab8_index():
    username = "anonymous"
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/login')
def login():
    return "Страница входа"

@lab8.route('/register')
def register():
    return "Страница регистрации"

@lab8.route('/articles')
def articles():
    return "Список статей"

@lab8.route('/create')
def create_article():
    return "Создание статьи"