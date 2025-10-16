from flask import Blueprint, render_template, request, redirect, url_for, session

lab4 = Blueprint('lab4', __name__, template_folder='templates')

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1_str = request.form.get('x1')
    x2_str = request.form.get('x2')
    if not x1_str or not x2_str:
        error = "Оба поля должны быть заполнены!"
        return render_template('lab4/div.html', error=error)

    try:
        x1 = int(x1_str)
        x2 = int(x2_str)
    except ValueError:
        error = "Поля должны содержать целые числа!"
        return render_template('lab4/div.html', error=error)

    if x2 == 0:
        error = "На ноль делить нельзя!"
        return render_template('lab4/div.html', error=error)

    result = x1 / x2

    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

def safe_int(val, default=None):
    """Преобразует строку в int или возвращает default, если невозможно."""
    if val == '' or val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return None


@lab4.route('/lab4/add')
def add():
    a = safe_int(request.args.get('a'), 0)
    b = safe_int(request.args.get('b'), 0)
    if a is None or b is None:
        result = "Ошибка: введите целые числа"
    else:
        result = a + b
    return render_template('lab4/arithmetic.html',
                           operation="Суммирование",
                           a=request.args.get('a', ''),
                           b=request.args.get('b', ''),
                           result=result,
                           show_form=True)


@lab4.route('/lab4/mul')
def mul():
    a = safe_int(request.args.get('a'), 1)
    b = safe_int(request.args.get('b'), 1)
    if a is None or b is None:
        result = "Ошибка: введите целые числа"
    else:
        result = a * b
    return render_template('lab4/arithmetic.html',
                           operation="Умножение",
                           a=request.args.get('a', ''),
                           b=request.args.get('b', ''),
                           result=result,
                           show_form=True)


@lab4.route('/lab4/sub')
def sub():
    a_str = request.args.get('a')
    b_str = request.args.get('b')
    if not a_str or not b_str:
        result = "Ошибка: оба поля должны быть заполнены"
    else:
        a = safe_int(a_str)
        b = safe_int(b_str)
        if a is None or b is None:
            result = "Ошибка: введите целые числа"
        else:
            result = a - b
    return render_template('lab4/arithmetic.html',
                           operation="Вычитание",
                           a=a_str or '',
                           b=b_str or '',
                           result=result,
                           show_form=True)


@lab4.route('/lab4/pow')
def power():
    a_str = request.args.get('a')
    b_str = request.args.get('b')
    if not a_str or not b_str:
        result = "Ошибка: оба поля должны быть заполнены"
    else:
        a = safe_int(a_str)
        b = safe_int(b_str)
        if a is None or b is None:
            result = "Ошибка: введите целые числа"
        elif a == 0 and b == 0:
            result = "Ошибка: 0⁰ не определено"
        else:
            try:
                result = a ** b
                if abs(result) > 10**10:
                    result = "Результат слишком большой"
            except OverflowError:
                result = "Результат слишком большой"
    return render_template('lab4/arithmetic.html',
                           operation="Возведение в степень",
                           a=a_str or '',
                           b=b_str or '',
                           result=result,
                           show_form=True)


tree_count = 0
MAX_TREES = 10  

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'plant' and tree_count < MAX_TREES:
            tree_count += 1
        elif operation == 'cut' and tree_count > 0:
            tree_count -= 1
        return redirect('/lab4/tree')

    return render_template('lab4/tree.html', tree_count=tree_count, max_trees=MAX_TREES)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит'},
    {'login': 'eve', 'password': 'secret', 'name': 'Ева Петрова'},
    {'login': 'charlie', 'password': 'pass123', 'name': 'Чарли Браун'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            user_login = session['login']
            user_name = next((u['name'] for u in users if u['login'] == user_login), user_login)
            return render_template('lab4/login.html', authorized=True, login=user_name, error=None)
        else:
            return render_template('lab4/login.html', authorized=False, login='', error=None)

    login_input = request.form.get('login')
    password = request.form.get('password')

    if not login_input:
        return render_template('lab4/login.html', authorized=False, login='', error='Не введён логин')
    if not password:
        return render_template('lab4/login.html', authorized=False, login=login_input, error='Не введён пароль')


    for user in users:
        if user['login'] == login_input and user['password'] == password:
            session['login'] = login_input  
            return redirect(url_for('lab4.login')) 

    return render_template('lab4/login.html', authorized=False, login=login_input, error='Неверные логин и/или пароль')


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)  
    return redirect(url_for('lab4.login'))