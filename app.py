from models import init_db, close_db

from flask import Flask, render_template

app = Flask(__name__)

# Ініціалізація бази даних
init_db(app)
app.teardown_appcontext(close_db)

@app.route('/')
def index():
    return render_template('index.html', title='Головна')

@app.route('/about')
def about():
    return render_template('about.html', title='Про нас')

@app.route('/services')
def services():
    return render_template('services.html', title='Послуги')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Контакти')

if __name__ == '__main__':
    app.run(debug=True)