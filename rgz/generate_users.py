import os
import random
from werkzeug.security import generate_password_hash
from models.db_model import db, User

full_names = [
    "Иванов Иван Иванович",
    "Петрова Мария Сергеевна",
    "Сидоров Алексей Дмитриевич",
    "Кузнецова Екатерина Андреевна",
    "Смирнов Дмитрий Владимирович",
    "Попова Ольга Николаевна",
    "Козлов Сергей Александрович",
    "Новикова Наталья Павловна",
    "Морозов Андрей Викторович",
    "Волкова Юлия Игоревна",
    "Федоров Михаил Олегович",
    "Белова Елена Романовна",
    "Андреев Владимир Степанович",
    "Соколова Татьяна Григорьевна",
    "Лебедев Павел Валерьевич",
    "Григорьева Анастасия Алексеевна",
    "Зайцев Николай Юрьевич",
    "Титова Дарья Максимовна",
    "Макаров Артём Ильич",
    "Власова Виктория Олеговна",
    "Фролов Роман Сергеевич",
    "Дмитриева Алина Владиславовна",
    "Соловьёв Станислав Михайлович",
    "Киселёва Полина Андреевна",
    "Степанов Григорий Викторович",
    "Николаева Ксения Дмитриевна",
    "Орлов Игорь Петрович",
    "Максимова Маргарита Станиславовна",
    "Борисов Борис Анатольевич",
    "Жукова Оксана Валерьевна"
]

service_types = [
    "Веб-дизайн", "Программирование", "Фотография", "Копирайтинг", "Видео-монтаж",
    "SEO-оптимизация", "SMM-менеджмент", "3D-моделирование", "Аудит сайтов",
    "Консультации", "Переводы", "Аналитика", "Иллюстрации", "Архитектура",
    "Маркетинг", "Бухгалтерия", "Юриспруденция", "Репетиторство"
]

def generate_users():
    if User.query.count() >= 30:
        return

    for i in range(30):
        username = f"user{i+1:02d}"
        if User.query.filter_by(username=username).first():
            continue

        name = full_names[i]
        service = random.choice(service_types)
        experience = random.randint(1, 15)
        price = random.randint(300, 5000)
        about = f"Профессиональный специалист в области {service.lower()}. Опыт - {experience} лет. Пишите на почту: {username}.mail.ru"

        user = User(
            username=username,
            password_hash=generate_password_hash("123456"),
            is_admin=False,
            is_visible=True,
            name=name,
            service_type=service,
            experience=experience,
            price=price,
            about=about
        )
        db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
