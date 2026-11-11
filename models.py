import sqlite3
from flask import g

DATABASE = 'db.sqlite'

def get_db():
    """Створює з'єднання з базою даних для поточного запиту"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Дозволяє читати рядки як словники
        g.db.execute('PRAGMA foreign_keys = ON')  # Увімкнення зовнішніх ключів
    return g.db

def close_db(e=None):
    """Закриває з'єднання з базою даних після завершення запиту"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Створює всі необхідні таблиці в базі даних, якщо їх ще немає"""
    with app.app_context():
        db = get_db()
        
        # 1. Таблиця відгуків (Рівень 1)
        db.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        
        # 2. Таблиця товарів/послуг (Рівень 1)
        db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
        ''')
        
        # Додаємо тестові послуги в базу, якщо їх там ще немає
        db.execute("INSERT OR IGNORE INTO products (id, title, price, description) VALUES (1, 'Веб-розробка', 5000.0, 'Розробка надійних серверних застосунків на Python із використанням Flask.');")
        db.execute("INSERT OR IGNORE INTO products (id, title, price, description) VALUES (2, 'Адаптивна верстка', 3000.0, 'Створення кросплатформових вебсторінок за допомогою Tailwind CSS.');")
        db.execute("INSERT OR IGNORE INTO products (id, title, price, description) VALUES (3, 'Шаблонізація Jinja2', 2500.0, 'Побудова динамічних та оптимізованих HTML-шаблонів з наслідуванням.');")

        # 3. Таблиця замовлень (Рівень 1)
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                status TEXT DEFAULT 'Новий',
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # 4. Таблиця користувачів з ролями (Твоє завдання — Рівень 3)
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'client'
            )
        ''')
        
        db.commit()