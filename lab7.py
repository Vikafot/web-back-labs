from flask import Blueprint, render_template, request, jsonify, current_app
from database import db_connect, db_close

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

def get_all_films():
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    if db_type == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return [dict(f) for f in films]


def get_film_by_id(film_id):
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    if db_type == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (film_id,))
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (film_id,))
    film = cur.fetchone()
    db_close(conn, cur)
    return dict(film) if film else None


def delete_film_by_id(film_id):
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    if db_type == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s", (film_id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?", (film_id,))
    success = cur.rowcount > 0
    db_close(conn, cur)
    return success


def update_film(film_id, title, title_ru, year, description):
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    if db_type == 'postgres':
        cur.execute(
            "UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s",
            (title, title_ru, year, description, film_id)
        )
    else:
        cur.execute(
            "UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?",
            (title, title_ru, year, description, film_id)
        )
    success = cur.rowcount > 0
    db_close(conn, cur)
    return success


def add_film_to_db(title, title_ru, year, description):
    conn, cur = db_connect()
    db_type = current_app.config['DB_TYPE']
    if db_type == 'postgres':
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id",
            (title, title_ru, year, description)
        )
        new_id = cur.fetchone()['id']
    else:
        cur.execute(
            "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
            (title, title_ru, year, description)
        )
        new_id = cur.lastrowid
    db_close(conn, cur)
    return new_id


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(get_all_films())


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    film = get_film_by_id(id)
    if not film:
        return jsonify({"error": "Film not found"}), 404
    return jsonify(film)


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    if not get_film_by_id(id):
        return jsonify({"error": "Film not found"}), 404
    delete_film_by_id(id)
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def edit_film(id):
    if not get_film_by_id(id):
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
    if len(description) > 2000:
        return jsonify({"description": "Описание не должно превышать 2000 символов"}), 400
    if not isinstance(year, int) or year < 1895 or year > 2025:
        return jsonify({"year": "Год должен быть от 1895 до 2025"}), 400

    if not title:
        title = title_ru

    update_film(id, title, title_ru, year, description)
    return jsonify(get_film_by_id(id))


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
    if len(description) > 2000:
        return jsonify({"description": "Описание не должно превышать 2000 символов"}), 400
    if not isinstance(year, int) or year < 1895 or year > 2025:
        return jsonify({"year": "Год должен быть от 1895 до 2025"}), 400

    if not title:
        title = title_ru

    new_id = add_film_to_db(title, title_ru, year, description)
    return jsonify(new_id)