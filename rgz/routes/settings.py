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
            name = request.form.get('name', '').strip()
            service_type = request.form.get('service_type', '').strip()
            experience = request.form.get('experience', '').strip()
            price = request.form.get('price', '').strip()
            about = request.form.get('about', '').strip()
            is_visible = 'is_visible' in request.form

            if not (name and service_type and experience and price):
                message = "Заполните все обязательные поля"
                message_type = "error"
                return render_template(
                    'settings.html',
                    user=target_user,
                    message=message,
                    message_type=message_type,
                    is_admin_edit=is_admin_edit
                )
            
            try:
                experience = int(experience)
                price = int(price)
                if experience < 0 or price <= 0:
                    raise ValueError
            except ValueError:
                message = "Стаж должен быть >= 0, цена > 0"
                message_type = "error"
                return render_template(
                    'settings.html',
                    user=target_user,
                    message=message,
                    message_type=message_type,
                    is_admin_edit=is_admin_edit
                )

            target_user.name = name
            target_user.service_type = service_type
            target_user.experience = experience
            target_user.price = price
            target_user.about = about
            target_user.is_visible = is_visible

            db.session.commit()
            message = "Анкета успешно обновлена"
            message_type = "success"

        elif 'delete_account' in request.form:
            db.session.delete(target_user)
            db.session.commit()
            is_self_deletion = (target_user.id == current_user.id)
            if is_self_deletion:
                session.pop('login', None)
                session.pop('is_admin', None)
            return redirect('/')

    return render_template(
        'settings.html',
        user=target_user,
        message=message,
        message_type=message_type,
        is_admin_edit=is_admin_edit
    )
