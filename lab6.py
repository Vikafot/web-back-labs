from flask import Blueprint, render_template, request, session, current_app
from database import db_connect, db_close

lab6 = Blueprint('lab6', __name__, template_folder='templates')

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        rows = cur.fetchall()

        if current_app.config['DB_TYPE'] == 'postgres':
            offices = [dict(row) for row in rows]
        else:
            offices = [dict(row) for row in rows]

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Unauthorized'},
                'id': id
            }

        office_number = data.get('params')
        if office_number is None:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32602, 'message': 'Параметр params обязателен'},
                'id': id
            }

        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM offices WHERE number = ?", (office_number,))
        row = cur.fetchone()

        if not row:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32602, 'message': f'Офис {office_number} не существует'},
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            office = dict(row)
        else:
            office = dict(zip([col[0] for col in cur.description], row))

        if office['tenant'] != '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 2, 'message': 'Already booked'},
                'id': id
            }

        cur.execute(
            "UPDATE offices SET tenant = %s WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres'
            else "UPDATE offices SET tenant = ? WHERE number = ?",
            (login, office_number)
        )
        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    elif data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Unauthorized'},
                'id': id
            }

        office_number = data.get('params')
        if office_number is None:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32602, 'message': 'Параметр params обязателен'},
                'id': id
            }

        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM offices WHERE number = ?", (office_number,))
        row = cur.fetchone()

        if not row:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32602, 'message': f'Офис {office_number} не существует'},
                'id': id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            office = dict(row)
        else:
            office = dict(zip([col[0] for col in cur.description], row))

        if office['tenant'] == '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 3, 'message': 'Office is not booked'},
                'id': id
            }

        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 4, 'message': 'Cannot cancel someone else\'s booking'},
                'id': id
            }

        cur.execute(
            "UPDATE offices SET tenant = %s WHERE number = %s" if current_app.config['DB_TYPE'] == 'postgres'
            else "UPDATE offices SET tenant = ? WHERE number = ?",
            ('', office_number)
        )
        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': id
    }
