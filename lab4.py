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
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'м'},
    {'login': 'eve', 'password': 'secret', 'name': 'Ева Петрова', 'gender': 'ж'},
    {'login': 'anna', 'password': 'qwerty', 'name': 'Анна Сидорова', 'gender': 'ж'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            user_login = session['login']
            user = next((u for u in users if u['login'] == user_login), None)
            if user:
                return render_template('lab4/login.html', authorized=True, login=user['name'], error=None)
            else:
                session.pop('login', None)
                return render_template('lab4/login.html', authorized=False, login='', error=None)
        else:
            return render_template('lab4/login.html', authorized=False, login='', error=None)

    login_input = request.form.get('login') or ''  
    password = request.form.get('password') or ''

    if not login_input.strip():
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


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html', result=None)
    temp_str = request.form.get('temperature')
  
    if not temp_str:
        result = {
            'message': 'ошибка: не задана температура',
            'snowflakes': 0,
            'error': True
        }
        return render_template('lab4/fridge.html', result=result)

    try:
        temp = float(temp_str)
    except ValueError:
        result = {
            'message': 'ошибка: температура должна быть числом',
            'snowflakes': 0,
            'error': True
        }
        return render_template('lab4/fridge.html', result=result)

    if temp < -12:
        result = {
            'message': 'не удалось установить температуру — слишком низкое значение',
            'snowflakes': 0,
            'error': True
        }
    elif temp > -1:
        result = {
            'message': 'не удалось установить температуру — слишком высокое значение',
            'snowflakes': 0,
            'error': True
        }
    elif -12 <= temp <= -9:
        result = {
            'message': f'Установлена температура: {temp}°С',
            'snowflakes': 3,
            'error': False
        }
    elif -8 <= temp <= -5:
        result = {
            'message': f'Установлена температура: {temp}°С',
            'snowflakes': 2,
            'error': False
        }
    elif -4 <= temp <= -1:
        result = {
            'message': f'Установлена температура: {temp}°С',
            'snowflakes': 1,
            'error': False
        }
    else:
        result = {
            'message': 'не удалось установить температуру — значение вне допустимых диапазонов',
            'snowflakes': 0,
            'error': True
        }
    return render_template('lab4/fridge.html', result=result)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain.html', result=None)

    grain_type = request.form.get('grain')
    weight_str = request.form.get('weight')

    grain_prices = {
        'barley': 12000,
        'oats': 8500,
        'wheat': 9000,
        'rye': 15000
    }

    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    if not grain_type or grain_type not in grain_prices:
        result = {'error': 'Не выбран тип зерна'}
        return render_template('lab4/grain.html', result=result)

    if not weight_str:
        result = {'error': 'Вес не указан'}
        return render_template('lab4/grain.html', result=result)

    try:
        weight = float(weight_str)
    except ValueError:
        result = {'error': 'Вес должен быть числом'}
        return render_template('lab4/grain.html', result=result)

    if weight <= 0:
        result = {'error': 'Вес должен быть больше нуля'}
        return render_template('lab4/grain.html', result=result)

    if weight > 100:
        result = {'error': 'Такого объёма сейчас нет в наличии'}
        return render_template('lab4/grain.html', result=result)

    price_per_ton = grain_prices[grain_type]
    total = weight * price_per_ton
    discount_applied = False
    discount_amount = 0

    if weight > 10:
        discount_applied = True
        discount_amount = total * 0.10
        total -= discount_amount

    result = {
        'success': True,
        'grain_name': grain_names[grain_type],
        'weight': weight,
        'total': round(total, 2),
        'discount_applied': discount_applied,
        'discount_amount': round(discount_amount, 2)
    }
    return render_template('lab4/grain.html', result=result)