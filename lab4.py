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