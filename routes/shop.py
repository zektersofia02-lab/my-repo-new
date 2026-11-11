from flask import Blueprint, render_template
from models import get_db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/services')
def services():
    db = get_db()
    cursor = db.execute('SELECT * FROM products')
    items = cursor.fetchall()
    
    return render_template('services.html', services=items, title='Послуги та каталог')