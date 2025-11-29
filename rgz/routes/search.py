from flask import Blueprint, render_template, session, redirect, request
from models.db_model import db, User

search = Blueprint('search', __name__)

@search.route('/search')
def search_handler():
    name = request.args.get('name', '').strip()
    service_type = request.args.get('service_type', '').strip()
    exp_from = request.args.get('exp_from', type=int)
    exp_to = request.args.get('exp_to', type=int)
    price_from = request.args.get('price_from', type=int)
    price_to = request.args.get('price_to', type=int)
    page = request.args.get('page', 1, type=int)

    query = User.query.filter_by(is_visible=True)

    if name:
        query = query.filter(User.name.ilike(f'%{name}%'))
    if service_type:
        query = query.filter(User.service_type.ilike(f'%{service_type}%'))
    if exp_from is not None:
        query = query.filter(User.experience >= exp_from)
    if exp_to is not None:
        query = query.filter(User.experience <= exp_to)
    if price_from is not None:
        query = query.filter(User.price >= price_from)
    if price_to is not None:
        query = query.filter(User.price <= price_to)

    pagination = query.paginate(page=page, per_page=5, error_out=False)

    return render_template(
        'search.html',
        results=pagination.items,
        pagination=pagination,
        name=name,
        service_type=service_type,
        exp_from=exp_from,
        exp_to=exp_to,
        price_from=price_from,
        price_to=price_to
    )
