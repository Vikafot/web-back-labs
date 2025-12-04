from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы найти планету с подходящими условиями."
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "В будущем человечество порабощено машинами, которые используют людей как источник энергии, погружая их в виртуальную реальность — Матрицу."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Профессиональный вор извлекает секреты из подсознания жертв во сне. Ему предлагают почти невозможную задачу — внедрить идею."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Банкир Энди Дюфрейн обвинён в убийстве и отправлен в тюрьму, где сохраняет надежду и строит план побега."
    },
    {
        "title": "Spirited Away",
        "title_ru": "Унесённые призраками",
        "year": 2001,
        "description": "Девочка Чихиро попадает в мир духов и должна работать в бане, чтобы спасти родителей и найти путь домой."
    }
]


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def edit_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"description": "Некорректные данные"}), 400

    title_ru = data.get("title_ru", "").strip()
    title = data.get("title", "").strip()
    year = data.get("year")
    description = data.get("description", "").strip()

    if not title_ru:
        return jsonify({"title_ru": "Русское название обязательно"}), 400
    if not description:
        return jsonify({"description": "Описание обязательно"}), 400
    if not isinstance(year, int) or year < 1895 or year > 2025:
        return jsonify({"year": "Год должен быть от 1895 до 2025"}), 400

    if not title:
        title = title_ru

    films[id] = {
        "title": title,
        "title_ru": title_ru,
        "year": year,
        "description": description
    }
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    if not data:
        return jsonify({"description": "Некорректные данные"}), 400

    title_ru = data.get("title_ru", "").strip()
    title = data.get("title", "").strip()
    year = data.get("year")
    description = data.get("description", "").strip()

    if not title_ru:
        return jsonify({"title_ru": "Русское название обязательно"}), 400
    if not description:
        return jsonify({"description": "Описание обязательно"}), 400
    if not isinstance(year, int) or year < 1895 or year > 2025:
        return jsonify({"year": "Год должен быть от 1895 до 2025"}), 400

    if not title:
        title = title_ru

    new_film = {
        "title": title,
        "title_ru": title_ru,
        "year": year,
        "description": description
    }
    films.append(new_film)
    return jsonify(len(films) - 1)