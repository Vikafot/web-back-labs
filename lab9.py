from flask import Blueprint, render_template, session, jsonify, request
import random
from hashlib import md5
import uuid

lab9 = Blueprint('lab9', __name__)

OPENED_BOXES_GLOBAL = set()
MAX_BOXES_PER_USER = 3

GIFT_DATA = [
    {"message": "С Новым годом! Пусть мечты сбываются!", "image": "/static/lab9/игрушка1.jpg"},
    {"message": "Желаю здоровья, счастья и удачи!", "image": "/static/lab9/игрушка2.jpg"},
    {"message": "Пусть в доме будет тепло, а в сердце — любовь!", "image": "/static/lab9/игрушка3.jpg"},
    {"message": "Счастья тебе и вдохновения в новом году!", "image": "/static/lab9/игрушка4.jpg"},
    {"message": "Пусть Дед Мороз исполнит все твои желания!", "image": "/static/lab9/игрушка5.jpg"},
    {"message": "Новый год — время чудес! Пусть они начнутся с тебя!", "image": "/static/lab9/игрушка6.jpg"},
    {"message": "Пусть удача будет твоим верным спутником!", "image": "/static/lab9/игрушка7.jpg"},
    {"message": "Желаю радости, тепла и сказки в каждом дне!", "image": "/static/lab9/игрушка8.jpg"},
    {"message": "Пусть настроение будет праздничным весь год!", "image": "/static/lab9/игрушка9.jpg"},
    {"message": "С Новым годом! Пусть всё плохое останется в прошлом!", "image": "/static/lab9/игрушка10.jpg"},
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
    return render_template('lab9/index.html', positions=positions)

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
