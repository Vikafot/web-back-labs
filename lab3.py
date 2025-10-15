from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'аноним')
    age = request.cookies.get('age', 'неизвестный')
    name_color = request.cookies.get('name_color', 'black')
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age','20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    errors = {}
    if user == '':  
        errors['user'] = 'Заполните поле!'
    if age == '':  
        errors['age'] = 'Заполните поле!'
    return render_template('lab3/form1.html',
                           user=user,
                           age=age,
                           sex=sex,
                           errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 'неизвестно')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    text_color = request.args.get('text_color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if text_color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if text_color:
            resp.set_cookie('text_color', text_color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    text_color = request.cookies.get('text_color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_style = request.cookies.get('font_style', 'normal')

    return render_template('lab3/settings.html',
                           text_color=text_color,
                           bg_color=bg_color,
                           font_size=font_size,
                           font_style=font_style)


@lab3.route('/lab3/ticket_form')
def ticket_form():
    return render_template('lab3/ticket_form.html')


@lab3.route('/lab3/ticket')
def ticket():
    errors = []

    fullname = request.args.get('fullname', '').strip()
    berth = request.args.get('berth', '')
    linen = request.args.get('linen') is not None
    luggage = request.args.get('luggage') is not None
    age_str = request.args.get('age', '').strip()
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    travel_date = request.args.get('travel_date', '').strip()
    insurance = request.args.get('insurance') is not None

    if not fullname:
        errors.append("Укажите ФИО пассажира.")
    if not berth:
        errors.append("Выберите тип полки.")
    if not age_str:
        errors.append("Укажите возраст.")
    else:
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors.append("Возраст должен быть от 1 до 120 лет.")
        except ValueError:
            errors.append("Возраст должен быть числом.")
    if not departure:
        errors.append("Укажите пункт выезда.")
    if not destination:
        errors.append("Укажите пункт назначения.")
    if not travel_date:
        errors.append("Укажите дату поездки.")

    if errors:
        return render_template('lab3/ticket_form.html', errors=errors)

    is_child = age < 18
    base_price = 700 if is_child else 1000
    total = base_price

    if berth in ['нижняя', 'нижняя боковая']:
        total += 100
    if linen:
        total += 75
    if luggage:
        total += 250
    if insurance:
        total += 150

    return render_template('lab3/ticket.html',
                           fullname=fullname,
                           berth=berth,
                           linen=linen,
                           luggage=luggage,
                           age=age,
                           departure=departure,
                           destination=destination,
                           travel_date=travel_date,
                           insurance=insurance,
                           is_child=is_child,
                           total_price=total)