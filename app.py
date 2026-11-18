from flask import Flask, render_template  # <--- Додали Flask
from models import init_db, close_db
from routes.shop import shop_bp 
from routes.admin import admin_bp  # <--- 1. Імпортуємо твою адмінку

app = Flask(__name__)

# ДОДАЄМО СЕКРЕТНИЙ КЛЮЧ ДЛЯ РОБОТИ ПОВІДОМЛЕНЬ ТА СЕСІЙ
app.secret_key = 'super-secret-key-12345'

app.config['DATABASE'] = 'db.sqlite'

# Ініціалізація бази даних
init_db(app)
app.teardown_appcontext(close_db)

# Реєструємо маршрути магазину/послуг
app.register_blueprint(shop_bp)

# Реєструємо твою адмін-панель категорій!
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html', title='Головна')

@app.route('/about')
def about():
    return render_template('about.html', title='Про нас')

import sqlite3
from flask import request, redirect, url_for

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Підключаємося до бази даних і записуємо відгук
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()
        
        return redirect(url_for('contact'))
        
    return render_template('contact.html', title='Контакти')

if __name__ == '__main__':
    app.run(debug=True)