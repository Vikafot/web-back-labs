from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__, 
                 template_folder='templates',
                 static_folder='static')

@lab5.route('/lab5/')
def main():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vika_fot_knowledge_base_db',
            user='vika_fot_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '').strip()

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
            (login, password_hash, real_name)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
            (login, password_hash, real_name)
        )
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/login_success.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')
 
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи не могут быть пустыми.")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?", (login, ))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(login_id, title, article_text) VALUES (%s, %s, %s)",
            (login_id, title, article_text)
        )
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text) VALUES (?, ?, ?)",
            (login_id, title, article_text)
        )

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?", (login, ))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite, id DESC;",
            (login_id,)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite, id DESC;",
            (login_id,)
        )
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?", (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return redirect('/lab5')
    login_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s", (article_id, login_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?", (article_id, login_id))
    article = cur.fetchone()
    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав на её редактирование", 403

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error="Название и текст не могут быть пустыми")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s AND login_id=%s",
            (title, article_text, is_favorite, is_public, article_id, login_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? WHERE id=? AND login_id=?",
            (title, article_text, is_favorite, is_public, article_id, login_id)
    )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?", (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return "Пользователь не найден", 404
    login_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND login_id=%s", (article_id, login_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND login_id=?", (article_id, login_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users_list.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT login, real_name FROM users WHERE login=?", (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return "Пользователь не найден", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    new_real_name = request.form.get('real_name', '').strip()
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    error = None

    if new_real_name != user['real_name']:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s", (new_real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?", (new_real_name, login))

    if old_password or new_password or confirm_password:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT password FROM users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT password FROM users WHERE login=?", (login,))
        pwd_hash = cur.fetchone()['password']

        if not check_password_hash(pwd_hash, old_password):
            error = "Неверный текущий пароль."
        elif not new_password:
            error = "Новый пароль не может быть пустым."
        elif new_password != confirm_password:
            error = "Пароли не совпадают."
        else:
            new_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET password=%s WHERE login=%s", (new_hash, login))
            else:
                cur.execute("UPDATE users SET password=? WHERE login=?", (new_hash, login))

    if error:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, error=error)

    db_close(conn, cur)
    return redirect('/lab5/profile?updated=1')

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.title, a.article_text, u.login
            FROM articles a
            JOIN users u ON a.login_id = u.id
            WHERE a.is_public = TRUE
            ORDER BY a.id DESC
        """)
    else:
        cur.execute("""
            SELECT a.title, a.article_text, u.login
            FROM articles a
            JOIN users u ON a.login_id = u.id
            WHERE a.is_public = 1
            ORDER BY a.id DESC
        """)

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)
