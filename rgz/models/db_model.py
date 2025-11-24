from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_visible = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(100))
    service_type = db.Column(db.String(50))
    experience = db.Column(db.Integer)
    price = db.Column(db.Integer)
    about = db.Column(db.Text)
