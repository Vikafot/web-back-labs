from flask import Blueprint, render_template, request

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