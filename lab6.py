from flask import Blueprint, render_template

lab6 = Blueprint('lab6', __name__, template_folder='templates')

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')