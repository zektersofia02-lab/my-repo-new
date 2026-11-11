from flask import Flask, render_template  # <--- Додали Flask
from models import init_db, close_db
from routes.shop import shop_bp 

app = Flask(__name__)

# ДОДАЄМО СЕКРЕТНИЙ КЛЮЧ ДЛЯ РОБОТИ ПОВІДОМЛЕНЬ ТА СЕСІЙ
app.secret_key = 'super-secret-key-12345'

app.config['DATABASE'] = 'db.sqlite'

# Ініціалізація бази даних
init_db(app)
app.teardown_appcontext(close_db)

# Реєструємо маршрути магазину/послуг
app.register_blueprint(shop_bp)

@app.route('/')
def index():
    return render_template('index.html', title='Головна')

@app.route('/about')
def about():
    return render_template('about.html', title='Про нас')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Контакти')

if __name__ == '__main__':
    app.run(debug=True)