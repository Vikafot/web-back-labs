import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS offices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER UNIQUE NOT NULL,
        tenant TEXT DEFAULT '',
        price INTEGER NOT NULL
    )
''')

for i in range(1, 11):
    cursor.execute('''
        INSERT OR IGNORE INTO offices (number, tenant, price)
        VALUES (?, ?, ?)
    ''', (i, "", 900 + i * 3))

conn.commit()
conn.close()

print(" Таблица 'offices' создана и заполнена.")