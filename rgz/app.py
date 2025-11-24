import os
from flask import Flask
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from models.db_model import db, User

load_dotenv()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

_initialized = False

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rgz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.before_request
    def initialize_app():
        global _initialized
        if not _initialized:
            with app.app_context():
                db.create_all()
                create_admin()
            _initialized = True

    @app.route('/')
    def index():
        return "Приложение работает! ФИО: Фот Виктория Владимировна | Группа: ФБИ-33"

    return app


def create_admin():
    if not User.query.filter_by(username=ADMIN_USERNAME).first():
        admin = User(
            username=ADMIN_USERNAME,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True,
            is_visible=True,
            name='Администратор',
            service_type='admin',
            experience=10,
            price=0,
            about='Учётная запись администратора'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
