from flask import Blueprint, render_template
from models.db_model import db, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.filter_by(is_visible=True, is_admin=False).all()
    return render_template('main-page.html', all_users=users)
