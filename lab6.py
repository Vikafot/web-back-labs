from flask import Blueprint, render_template, request, session
import sqlite3

lab6 = Blueprint('lab6', __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  
    return conn

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    if data['method'] == 'info':
        conn = get_db_connection()
        offices = conn.execute('SELECT number, tenant, price FROM offices ORDER BY number').fetchall()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': [dict(row) for row in offices],
            'id': id
        }

    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data.get('params')
        if office_number is None:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Параметр params обязателен'
                },
                'id': id
            }

        conn = get_db_connection()
        office = conn.execute('SELECT * FROM offices WHERE number = ?', (office_number,)).fetchone()

        if not office:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': f'Офис {office_number} не существует'
                },
                'id': id
            }

        if office['tenant'] != '':
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }

        conn.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        conn.commit()
        conn.close()

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
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data.get('params')
        if office_number is None:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Параметр params обязателен'
                },
                'id': id
            }

        conn = get_db_connection()
        office = conn.execute('SELECT * FROM offices WHERE number = ?', (office_number,)).fetchone()

        if not office:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': f'Офис {office_number} не существует'
                },
                'id': id
            }

        if office['tenant'] == '':
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not booked'
                },
                'id': id
            }

        if office['tenant'] != login:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Cannot cancel someone else\'s booking'
                },
                'id': id
            }
        conn.execute('UPDATE offices SET tenant = "" WHERE number = ?', (office_number,))
        conn.commit()
        conn.close()

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }