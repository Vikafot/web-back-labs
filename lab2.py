from flask import Blueprint, render_template, redirect, url_for, abort, request

lab2 = Blueprint('lab2', __name__)


flower_list = [
    {'name': 'роза', 'price': '130'},
    {'name': 'тюльпан', 'price': '110'},
    {'name': 'незабудка', 'price': '95'},
    {'name': 'ромашка', 'price': '80'}
]

books = [
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "genre": "Антиутопия",
        "pages": 328
    },
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "genre": "Фантастика, сатира",
        "pages": 480
    },
    {
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
        "genre": "Психологический роман",
        "pages": 592
    },
    {
        "title": "Гарри Поттер и философский камень",
        "author": "Дж. К. Роулинг",
        "genre": "Фэнтези",
        "pages": 432
    },
    {
        "title": "Война и мир",
        "author": "Лев Толстой",
        "genre": "Исторический роман",
        "pages": 1225
    },
    {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "genre": "Роман",
        "pages": 864
    },
    {
        "title": "Гордость и предубеждение",
        "author": "Джейн Остин",
        "genre": "Роман",
        "pages": 432
    },
    {
        "title": "Три товарища",
        "author": "Эрих Мария Ремарк",
        "genre": "Роман",
        "pages": 416
    },
    {
        "title": "Алхимик",
        "author": "Пауло Коэльо",
        "genre": "Философская притча",
        "pages": 192
    },
    {
        "title": "451 градус по Фаренгейту",
        "author": "Рэй Брэдбери",
        "genre": "Антиутопия",
        "pages": 256
    },
    {
        "title": "Шерлок Холмс: Исследования",
        "author": "Артур Конан Дойл",
        "genre": "Детектив",
        "pages": 352
    }
]

cats = [
    {
        "name": "Британский короткошёрстный",
        "description": "Кот с плюшевой шерстью и круглыми глазами.",
        "image": "british.png"
    },
    {
        "name": "Сиамский кот",
        "description": "Элегантный кот с голубыми глазами и темными отметинами.",
        "image": "siamski.png"
    },
    {
        "name": "Мейн-кун",
        "description": "Один из самых крупных домашних котов с кисточками на ушах.",
        "image": "meinkun.png"
    },
    {
        "name": "Рэгдолл",
        "description": "Спокойный и ласковый кот с голубыми глазами.",
        "image": "ragdoll.png"
    },
    {
        "name": "Сфинкс",
        "description": "Лысый кот с необычной внешностью и теплой кожей.",
        "image": "sphynx.png"
    },
    {
        "name": "Шотландская вислоухая",
        "description": "Она просто милая.",
        "image": "scotland.png"
    },
    {
        "name": "Бенгальская",
        "description": "Мяу",
        "image": "bengal.png"
    },
    {
        "name": "Персидская",
        "description": "Аристократ с длинной шерстью и приплюснутой мордочкой. Спокойная, но требует регулярного ухода за шерстью.",
        "image": "persian.png"
    },
    {
        "name": "Абиссинская",
        "description": "Активная и любопытная кошка с тиккированной шерстью, напоминающей шкуру дикого зверя.",
        "image": "abyssinian.png"
    },
    {
        "name": "Саванна",
        "description": "Гибрид домашней кошки и сервала. Высокая, стройная, с большими ушами и диким окрасом.",
        "image": "savanna.png"
    },
    {
        "name": "Ориентальная",
        "description": "Стройная кошка с большими ушами и множеством вариантов окраса. Очень умная и разговорчивая.",
        "image": "prikol.png"
    },
    {
        "name": "Русская голубая",
        "description": "Изящная кошка с серебристо-голубой шерстью и изумрудными глазами. Скромная и чистоплотная.",
        "image": "russian.png"
    },
    {
        "name": "Норвежская лесная",
        "description": "Мощная кошка с густой водонепроницаемой шерстью. Отлично лазает по деревьям и любит природу.",
        "image": "norwegian.png"
    },
    {
        "name": "Сибирская",
        "description": "Русская аборигенная порода с гипоаллергенной шерстью. Умная, сильная и преданная.",
        "image": "siberian.png"
    },
    {
        "name": "Экзотическая короткошёрстная",
        "description": "«Перс с короткой шерстью». Спокойная, милая и требует меньше ухода, чем персидская.",
        "image": "exotic.png"
    },
    {
        "name": "Хайленд-фолд",
        "description": "Шотландская вислоухая кошка с полудлинной шерстью. Милая, игривая и очень фотогеничная.",
        "image": "highland.png"
    },
    {
        "name": "Скоттиш-фолд",
        "description": "Знаменита своими загнутыми вперёд ушками. Добрая, спокойная и отлично ладит с детьми.",
        "image": "fold.png"
    },
    {
        "name": "Корниш-рекс",
        "description": "Кошка с волнистой шерстью и изящным телом. Очень активна, любит тепло и общение.",
        "image": "kornish.png"
    },
    {
        "name": "Девон-рекс",
        "description": "Похожа на эльфа: большие уши, большие глаза и кудрявая шерсть. Игривая и ласковая.",
        "image": "devon.png"
    },
    {
        "name": "Тойгер",
        "description": "Создана, чтобы походить на тигра! Имеет полосатый окрас и дружелюбный характер.",
        "image": "toiger.png"
    },
]


@lab2.route('/lab2/')
def lab2_index():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'


@lab2.route('/lab2/a')
def a2():
    return 'без слэша'


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    return render_template('lab2/flower-item.html',
                           flower_id=flower_id,
                           name=flower_list[flower_id]['name'],
                           price=flower_list[flower_id]['price'])


@lab2.route('/lab2/flowers/list')
def get_flowers_list():
    return render_template('lab2/flowers-list.html', flower_list=flower_list)


@lab2.route('/lab2/flowers/clear')
def clear_flowers_list():
    flower_list.clear()
    return render_template('lab2/clear-flowers.html')


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return render_template('lab2/add-flowers.html', name=name, price=price)


@lab2.route('/lab2/delete_flower/<int:id>')
def delete_flower(id):
    if id < 0 or id >= len(flower_list):
        abort(404)
    del flower_list[id]
    return redirect('/lab2/flowers/list')


@lab2.route('/lab2/add_flower/')
def empty_flower_name():
    abort(400, description='Вы не задали имя цветка.')


@lab2.route('/lab2/example')
def example():
    name = "Фот Виктория"
    lab_num = 2
    group = "ФБИ-33"
    course = 3
    fruits = [
        {'name': 'яблоки', 'price': '100'},
        {'name': 'груши', 'price': '120'},
        {'name': 'апельсины', 'price': '80'},
        {'name': 'мандарины', 'price': '95'},
        {'name': 'манго', 'price': '321'},
    ]
    return render_template('lab2/example.html', name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
@lab2.route('/lab2/calc/<int:num1>/')
@lab2.route('/lab2/calc/<int:num1>/<int:num2>')
def calculate(num1=1, num2=1):
    add = num1 + num2
    sub = num1 - num2
    mul = num1 * num2
    if num2 == 0:
        div = "Ошибка: деление на ноль"
    else:
        div = num1 / num2
    power = num1 ** num2

    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Калькулятор — {num1} и {num2}</title>
</head>
<body>
    <h2>Математические операции с {num1} и {num2}</h2>
    <ul>
        <li>Сложение: {num1} + {num2} = {add}</li>
        <li>Вычитание: {num1} - {num2} = {sub}</li>
        <li>Умножение: {num1} * {num2} = {mul}</li>
        <li>Деление: {num1} / {num2} = {div}</li>
        <li>Возведение в степень: {num1}<sup>{num2}</sup> = {power}</li>
    </ul>
    <a href="/lab2/">Вернуться на главную</a>
</body>
</html>
'''


@lab2.route('/lab2/books')
def get_books_list():
    return render_template('lab2/books.html', books=books)


@lab2.route('/lab2/cats')
def get_cats_list():
    return render_template('lab2/cats.html', cats=cats, dir_path='cats_images/')