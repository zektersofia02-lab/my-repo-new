from flask import Flask, render_template
from models import init_db, close_db
from routes.shop import shop_bp  # <--- Додали імпорт твого модуля

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'

# Ініціалізація бази даних
init_db(app)
app.teardown_appcontext(close_db)

# Реєструємо маршрути магазину/послуг
app.register_blueprint(shop_bp)  # <--- Зареєстрували блупринт

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