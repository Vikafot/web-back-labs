from flask import Blueprint, render_template, session, redirect, request
from models.db_model import db, User

settings = Blueprint('settings', __name__)

@settings.route('/settings', methods=['GET', 'POST'])
@settings.route('/settings/<int:user_id>', methods=['GET', 'POST'])
def settings_handler(user_id=None):
    if 'login' not in session:
        return redirect('/login')
    
    current_user = User.query.filter_by(username=session['login']).first()
    if not current_user:
        return redirect('/login')

    message = None
    message_type = None

    if user_id is None:
        target_user = current_user
        is_admin_edit = False
    else:
        if not current_user.is_admin:
            return redirect('/settings')
        target_user = User.query.filter_by(id=user_id).first()
        if not target_user:
            return redirect('/')
        is_admin_edit = True

    if request.method == 'POST':
        if not is_admin_edit and user_id is not None:
            return redirect('/settings')

        if 'update_profile' in request.form:
            target_user.name = request.form.get('name', '').strip()
            target_user.service_type = request.form.get('service_type', '').strip()
            target_user.experience = int(request.form.get('experience') or 0)
            target_user.price = int(request.form.get('price') or 0)
            target_user.about = request.form.get('about', '').strip()
            target_user.is_visible = 'is_visible' in request.form
            
            if current_user.is_admin:
                target_user.is_admin = 'is_admin' in request.form

            db.session.commit()
            message = "Анкета успешно обновлена"
            message_type = "success"

        elif 'delete_account' in request.form:
            db.session.delete(target_user)
            db.session.commit()
            if not is_admin_edit:
                session.pop('login', None)
            return redirect('/')

    return render_template(
        'settings.html',
        user=target_user,
        message=message,
        message_type=message_type,
        is_admin_edit=is_admin_edit
    )
