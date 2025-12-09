from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
import random
from hashlib import md5
import uuid

lab9 = Blueprint('lab9', __name__, template_folder='templates')

OPENED_BOXES_GLOBAL = set()
MAX_BOXES_PER_USER = 3

GIFT_DATA = [
    {"message": "С Новым годом! Пусть мечты сбываются!", "image": "/static/lab9/игрушка1.jpg", "auth_only": False},
    {"message": "Желаю здоровья, счастья и удачи!", "image": "/static/lab9/игрушка2.jpg", "auth_only": False},
    {"message": "Пусть в доме будет тепло, а в сердце — любовь!", "image": "/static/lab9/игрушка3.jpg", "auth_only": False},
    {"message": "Счастья тебе и вдохновения в новом году!", "image": "/static/lab9/игрушка4.jpg", "auth_only": False},
    {"message": "Пусть Дед Мороз исполнит все твои желания!", "image": "/static/lab9/игрушка5.jpg", "auth_only": False},
    {"message": "Новый год — время чудес! Пусть они начнутся с тебя!", "image": "/static/lab9/игрушка6.jpg", "auth_only": True},
    {"message": "Пусть удача будет твоим верным спутником!", "image": "/static/lab9/игрушка7.jpg", "auth_only": True},
    {"message": "Желаю радости, тепла и сказки в каждом дне!", "image": "/static/lab9/игрушка8.jpg", "auth_only": True},
    {"message": "Пусть настроение будет праздничным весь год!", "image": "/static/lab9/игрушка9.jpg", "auth_only": False},
    {"message": "С Новым годом! Пусть всё плохое останется в прошлом!", "image": "/static/lab9/игрушка10.jpg", "auth_only": False},
]

def generate_positions_for_user(user_id, count=10, width=900, height=600, box_size=90):
    seed = int(md5(user_id.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    positions = []
    occupied = []
    attempts = 0
    max_attempts = count * 100
    while len(positions) < count and attempts < max_attempts:
        x = rng.randint(0, width - box_size)
        y = rng.randint(0, height - box_size)
        new_rect = (x, y, x + box_size, y + box_size)
        overlap = False
        for (x1, y1, x2, y2) in occupied:
            if not (new_rect[2] < x1 or new_rect[0] > x2 or new_rect[3] < y1 or new_rect[1] > y2):
                overlap = True
                break
        if not overlap:
            positions.append({"x": x, "y": y})
            occupied.append(new_rect)
        attempts += 1
    while len(positions) < count:
        x = rng.randint(0, width - box_size)
        y = rng.randint(0, height - box_size)
        positions.append({"x": x, "y": y})
    return positions

@lab9.route('/')
def gifts_page():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    user_id = session['user_id']
    positions = generate_positions_for_user(user_id)
    is_authenticated = current_user.is_authenticated
    return render_template('lab9/index.html', positions=positions, is_authenticated=is_authenticated)

@lab9.route('/api/open_gift', methods=['POST'])
def open_gift():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    user_id = session['user_id']

    opened_by_user = session.get('opened_boxes', [])
    if len(opened_by_user) >= MAX_BOXES_PER_USER:
        return jsonify({"error": "Вы уже открыли 3 подарка!"}), 403

    data = request.get_json()
    box_index = data.get('box_index')
    if box_index is None or not (0 <= box_index <= 9):
        return jsonify({"error": "Неверный номер коробки"}), 400

    if GIFT_DATA[box_index]["auth_only"] and not current_user.is_authenticated:
        return jsonify({"error": "Этот подарок доступен только авторизованным пользователям!"}), 403

    if box_index in OPENED_BOXES_GLOBAL:
        return jsonify({"error": "Эта коробка уже открыта другим пользователем!"}), 400

    OPENED_BOXES_GLOBAL.add(box_index)
    opened_by_user.append(box_index)
    session['opened_boxes'] = opened_by_user

    gift = GIFT_DATA[box_index]
    return jsonify({
        "message": gift["message"],
        "image": gift["image"]
    })

@lab9.route('/api/gift_status')
def gift_status():
    return jsonify({
        "opened_boxes": list(OPENED_BOXES_GLOBAL),
        "remaining": 10 - len(OPENED_BOXES_GLOBAL)
    })

@lab9.route('/api/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    global OPENED_BOXES_GLOBAL
    OPENED_BOXES_GLOBAL = set()
    session['opened_boxes'] = []
    return jsonify({"success": True})
