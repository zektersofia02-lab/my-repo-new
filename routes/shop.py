from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/services')
def services():
    """Каталог послуг з підтримкою пошуку та фільтрації"""
    db = get_db()
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        cursor = db.execute(
            "SELECT * FROM products WHERE title LIKE ? OR description LIKE ?", 
            (f'%{search_query}%', f'%{search_query}%')
        )
    else:
        cursor = db.execute('SELECT * FROM products')
        
    items = cursor.fetchall()
    return render_template('services.html', services=items, title='Послуги та каталог', search_query=search_query)


@shop_bp.route('/order/<int:product_id>', methods=['POST'])
def make_order(product_id):
    """Створення замовлення (кошик) та редирект на сторінку замовлень"""
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    
    if product:
        db.execute('INSERT INTO orders (product_id, status) VALUES (?, ?)', (product_id, 'Новий'))
        db.commit()
        flash(f'Успішно замовлено послугу "{product["title"]}"!', 'success')
    else:
        flash('Помилка: послугу не знайдено.', 'error')
        
    return redirect(url_for('shop.view_orders'))


@shop_bp.route('/orders')
def view_orders():
    """Сторінка кошика та перегляду замовлень із JOIN-запитом до бази даних"""
    db = get_db()
    orders_data = db.execute('''
        SELECT orders.id, products.title, products.price, orders.status 
        FROM orders 
        JOIN products ON orders.product_id = products.id
        ORDER BY orders.id DESC
    ''').fetchall()
    
    return render_template('orders.html', orders=orders_data)


@shop_bp.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    """Скасування (видалення) замовлення з кошика"""
    db = get_db()
    db.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    db.commit()
    flash('Замовлення успішно скасовано.', 'success')
    return redirect(url_for('shop.view_orders'))