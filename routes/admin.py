from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Створюємо блюпринт для адмінки
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row  # Щоб звертатися до колонок за іменами
    return conn

# Головна сторінка адмін-панелі з управлінням категоріями
@admin_bp.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            conn.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
        conn.close()
        return redirect(url_for('admin.manage_categories'))
    
    # Отримуємо список усіх категорій
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    return render_template('admin/categories.html', categories=categories)