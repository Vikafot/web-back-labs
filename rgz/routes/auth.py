from flask import Blueprint, render_template, redirect, request, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.db_model import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if 'login' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    name = request.form.get('name', '').strip()
    service_type = request.form.get('service_type', '').strip()
    experience = request.form.get('experience', '').strip()
    price = request.form.get('price', '').strip()
    about = request.form.get('about', '').strip()

    if not (login and password and name and service_type and experience and price):
        return render_template('register.html', error='Заполните все обязательные поля')

    if User.query.filter_by(username=login).first():
        return render_template('register.html', error="Такой пользователь уже существует")

    try:
        experience = int(experience)
        price = int(price)
        if experience < 0 or price <= 0:
            raise ValueError
    except ValueError:
        return render_template('register.html', error='Стаж должен быть >= 0, цена > 0')

    new_user = User(
        username=login,
        password_hash=generate_password_hash(password),
        name=name,
        service_type=service_type,
        experience=experience,
        price=price,
        about=about,
        is_visible=True
    )

    db.session.add(new_user)
    db.session.commit()

    session['login'] = login
    return redirect('/')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'login' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('login.html', error="Заполните поля")

    user = User.query.filter_by(username=login).first()
    if not user:
        return render_template('login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user.password_hash, password):
        return render_template('login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    return redirect('/')

@auth.route('/logout')
def logout():
    session.pop('login', None)
    return redirect('/')
