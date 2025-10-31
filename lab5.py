from flask import Blueprint, render_template

lab5 = Blueprint('lab5', __name__, 
                 template_folder='templates',
                 static_folder='static')

@lab5.route('/lab5/')
def main():
    return render_template('lab5/lab5.html', username='anonymous')