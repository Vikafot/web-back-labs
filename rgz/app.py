import os
from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from models.db_model import db, User
from routes import main, auth, settings, search
from generate_users import generate_users
load_dotenv()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rgz.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        generate_users()
        create_admin()

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(settings)
    app.register_blueprint(search)

def create_admin():
    if not ADMIN_PASSWORD:
        return
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
