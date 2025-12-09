from flask import Blueprint, render_template

lab9 = Blueprint('lab9', __name__, url_prefix='/lab9')

@lab9.route('/')
def main():
    return render_template('lab9/index.html')