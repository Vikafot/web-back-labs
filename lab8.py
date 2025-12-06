from flask import Blueprint, render_template, request, redirect
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash

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

@lab8.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/register.html', 
                               error='Имя пользователя не может быть пустым')

    if not password_form or not password_form.strip():
        return render_template('lab8/register.html', 
                               error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                            error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8')

@lab8.route('/articles')
def articles():
    return "Список статей"

@lab8.route('/create')
def create_article():
    return "Создание статьи"