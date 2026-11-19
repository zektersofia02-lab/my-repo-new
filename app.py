from flask import Flask, render_template, jsonify, request, redirect, url_for
from flasgger import Swagger  # <--- Додаємо Swagger (для документації /apidocs/)
import sqlite3

from models import init_db, close_db
from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.v1 import api_v1  # <--- Новий Blueprint версії API v1[cite: 1]
from routes.v2 import api_v2  # <--- Новий Blueprint версії API v2[cite: 1]

app = Flask(__name__)

# ДОДАЄМО СЕКРЕТНИЙ КЛЮЧ ДЛЯ РОБОТИ ПОВІДОМЛЕНЬ ТА СЕСІЙ
app.secret_key = 'super-secret-key-12345'

app.config['DATABASE'] = 'db.sqlite'

# Ініціалізація бази даних
init_db(app)
app.teardown_appcontext(close_db)

# Підключаємо Swagger UI (буде доступний за адресою /apidocs/)[cite: 1]
swagger = Swagger(app)

# Реєструємо існуючі маршрути
app.register_blueprint(shop_bp) 
app.register_blueprint(admin_bp)

# Реєструємо версії REST API (/api/v1/... та /api/v2/...)[cite: 1]
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)


@app.route('/')
def index():
    return render_template('index.html', title='Головна')


@app.route('/about')
def about():
    return render_template('about.html', title='Про нас')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )
        conn.commit()
        conn.close()

        return redirect(url_for('contact'))

    return render_template('contact.html', title='Контакти')


# Обробка помилок у форматі JSON (щоб API повертало JSON, а не HTML)[cite: 1]
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Некоректний запит', 'status': 400}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Ресурс не знайдено', 'status': 404}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Метод не дозволений', 'status': 405}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутрішня помилка сервера', 'status': 500}), 500


if __name__ == '__main__':
    app.run(debug=True)