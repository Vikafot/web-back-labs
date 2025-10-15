from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


products = [
    {"name": "iPhone 15", "price": 95000, "brand": "Apple", "color": "Чёрный"},
    {"name": "Samsung Galaxy S24", "price": 85000, "brand": "Samsung", "color": "Серебристый"},
    {"name": "Xiaomi 14", "price": 65000, "brand": "Xiaomi", "color": "Синий"},
    {"name": "Google Pixel 8", "price": 72000, "brand": "Google", "color": "Белый"},
    {"name": "Huawei P60", "price": 58000, "brand": "Huawei", "color": "Зелёный"},
    {"name": "OnePlus 12", "price": 68000, "brand": "OnePlus", "color": "Чёрный"},
    {"name": "Sony Xperia 1 V", "price": 92000, "brand": "Sony", "color": "Фиолетовый"},
    {"name": "Motorola Edge 40", "price": 45000, "brand": "Motorola", "color": "Красный"},
    {"name": "Nokia G42", "price": 18000, "brand": "Nokia", "color": "Серый"},
    {"name": "Realme GT Neo 5", "price": 42000, "brand": "Realme", "color": "Чёрный"},
    {"name": "Oppo Find X6", "price": 75000, "brand": "Oppo", "color": "Золотой"},
    {"name": "Vivo X90", "price": 62000, "brand": "Vivo", "color": "Синий"},
    {"name": "ASUS ROG Phone 7", "price": 88000, "brand": "ASUS", "color": "Чёрный"},
    {"name": "Nothing Phone (2)", "price": 55000, "brand": "Nothing", "color": "Белый"},
    {"name": "ZTE Axon 40", "price": 38000, "brand": "ZTE", "color": "Серый"},
    {"name": "iPhone 14", "price": 78000, "brand": "Apple", "color": "Синий"},
    {"name": "Samsung Galaxy A54", "price": 35000, "brand": "Samsung", "color": "Лимонный"},
    {"name": "Xiaomi Redmi Note 13", "price": 22000, "brand": "Xiaomi", "color": "Зелёный"},
    {"name": "Honor 90", "price": 48000, "brand": "Honor", "color": "Чёрный"},
    {"name": "iPhone SE (2022)", "price": 45000, "brand": "Apple", "color": "Белый"},
    {"name": "Poco F5", "price": 32000, "brand": "Poco", "color": "Синий"},
    {"name": "Infinix Zero 30", "price": 28000, "brand": "Infinix", "color": "Фиолетовый"},
]


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

@lab3.route('/lab3/clear-settings')
def clear_settings():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('text_color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('font_style', '', expires=0)
    return resp

@lab3.route('/lab3/products')
def products_search():
    global_min = min(p['price'] for p in products)
    global_max = max(p['price'] for p in products)

    min_price = request.args.get('min_price') or request.cookies.get('min_price')
    max_price = request.args.get('max_price') or request.cookies.get('max_price')

    def to_int(val):
        return int(val) if val and val.isdigit() else None

    min_val = to_int(min_price)
    max_val = to_int(max_price)

    if min_val is not None and max_val is not None:
        if min_val > max_val:
            min_val, max_val = max_val, min_val

    filtered = []
    for p in products:
        include = True
        if min_val is not None and p['price'] < min_val:
            include = False
        if max_val is not None and p['price'] > max_val:
            include = False
        if include:
            filtered.append(p)

    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered,
        min_price=min_val,
        max_price=max_val,
        global_min=global_min,
        global_max=global_max
    ))

    if request.args.get('action') == 'search':
        if min_val is not None:
            resp.set_cookie('min_price', str(min_val))
        if max_val is not None:
            resp.set_cookie('max_price', str(max_val))

    return resp


@lab3.route('/lab3/products/reset')
def products_reset():
    resp = make_response(redirect('/lab3/products'))
    resp.set_cookie('min_price', '', expires=0)
    resp.set_cookie('max_price', '', expires=0)
    return resp