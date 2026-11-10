from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Головна')

@app.route('/about')
def about():
    return render_template('about.html', title='Про нас')

@app.route('/services')
def services():
    return render_template('services.html', title='Послуги')

if __name__ == '__main__':
    app.run(debug=True)