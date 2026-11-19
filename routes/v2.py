from flask import Blueprint, jsonify, request
from models import get_db

api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")


@api_v2.route("/products", methods=["GET"])
def get_products_v2():
    """
    Отримати список товарів/послуг (v2)
    ---
    tags:
      - API v2 - Products
    responses:
      200:
        description: Список товарів/послуг у форматі v2
    """
    rows = get_db().execute("SELECT * FROM products").fetchall()
    products = [dict(row) for row in rows]
    return jsonify({
        "api_version": "v2",
        "count": len(products),
        "products": products,
    }), 200


@api_v2.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product_v2(product_id):
    """
    Оновити товар/послугу за ID (v2)
    ---
    tags:
      - API v2 - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        example: 1
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Оновлена назва"
            price:
              type: number
              example: 4200
            description:
              type: string
              example: "Оновлений опис"
    responses:
      200:
        description: Оновлений товар/послуга (v2)
      400:
        description: Некоректні дані
      404:
        description: Послугу/товар не знайдено
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON-тіло запиту"}), 400

    db = get_db()
    existing = db.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    if existing is None:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404

    title = data.get("title", existing["title"])
    price = data.get("price", existing["price"])
    description = data.get("description", existing["description"])

    if not title or not isinstance(price, (int, float)):
        return jsonify({"error": "Некоректні значення title або price"}), 400

    db.execute(
        "UPDATE products SET title = ?, price = ?, description = ? WHERE id = ?",
        (title, price, description, product_id),
    )
    db.commit()

    updated = db.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    return jsonify({"api_version": "v2", "product": dict(updated)}), 200


@api_v2.route("/orders/<int:order_id>", methods=["PATCH"])
def update_order_status_v2(order_id):
    """
    Оновити статус замовлення за ID (v2)
    ---
    tags:
      - API v2 - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        example: 1
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              example: "В обробці"
    responses:
      200:
        description: Оновлене замовлення (v2)
      400:
        description: Відсутнє поле status
      404:
        description: Замовлення не знайдено
    """
    data = request.get_json(silent=True)
    if not data or not data.get("status"):
        return jsonify({"error": "Потрібне поле status"}), 400

    db = get_db()
    cursor = db.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (data["status"], order_id),
    )
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Замовлення не знайдено"}), 404

    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return jsonify({"api_version": "v2", "order": dict(order)}), 200


@api_v2.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order_v2(order_id):
    """
    Видалити замовлення за ID (v2)
    ---
    tags:
      - API v2 - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      204:
        description: Успішно видалено
      404:
        description: Замовлення не знайдено
    """
    db = get_db()
    cursor = db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Замовлення не знайдено"}), 404
    return "", 204
@api_v2.route("/products/<int:product_id>", methods=["GET"])
def get_product_v2(product_id):
    """
    Отримати товар/послугу за ID (v2)
    ---
    tags:
      - API v2 - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Дані товару/послуги (v2)
      404:
        description: Послугу/товар не знайдено
    """
    row = get_db().execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return jsonify({"api_version": "v2", "product": dict(row)}), 200


@api_v2.route("/products", methods=["POST"])
def create_product_v2():
    """
    Створити новий товар/послугу (v2)
    ---
    tags:
      - API v2 - Products
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - price
          properties:
            title:
              type: string
              example: "Інтернет-магазин"
            price:
              type: number
              example: 8500
            description:
              type: string
              example: "Опис послуги"
    responses:
      201:
        description: Створений товар/послуга (v2)
      400:
        description: Некоректні дані
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON-тіло запиту"}), 400

    title = data.get("title")
    price = data.get("price")
    description = data.get("description", "")

    if not title or not isinstance(price, (int, float)):
        return jsonify({"error": "Некоректні значення title або price"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO products (title, price, description) VALUES (?, ?, ?)",
        (title, price, description),
    )
    db.commit()

    created = db.execute(
        "SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify({"api_version": "v2", "product": dict(created)}), 201


@api_v2.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product_v2(product_id):
    """
    Видалити товар/послугу за ID (v2)
    ---
    tags:
      - API v2 - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      204:
        description: Успішно видалено
      404:
        description: Послугу/товар не знайдено
    """
    db = get_db()
    cursor = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return "", 204


@api_v2.route("/orders", methods=["GET"])
def get_orders_v2():
    """
    Отримати список замовлень (v2)
    ---
    tags:
      - API v2 - Orders
    responses:
      200:
        description: Список замовлень у форматі v2
    """
    rows = get_db().execute("SELECT * FROM orders").fetchall()
    orders = [dict(row) for row in rows]
    return jsonify({
        "api_version": "v2",
        "count": len(orders),
        "orders": orders,
    }), 200


@api_v2.route("/orders/<int:order_id>", methods=["GET"])
def get_order_v2(order_id):
    """
    Отримати замовлення за ID (v2)
    ---
    tags:
      - API v2 - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Дані замовлення (v2)
      404:
        description: Замовлення не знайдено
    """
    row = get_db().execute(
        "SELECT * FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Замовлення не знайдено"}), 404
    return jsonify({"api_version": "v2", "order": dict(row)}), 200


@api_v2.route("/orders", methods=["POST"])
def create_order_v2():
    """
    Створити нове замовлення (v2)
    ---
    tags:
      - API v2 - Orders
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - product_id
          properties:
            product_id:
              type: integer
              example: 1
            status:
              type: string
              example: "Нове"
    responses:
      201:
        description: Створене замовлення (v2)
      400:
        description: Некоректні дані
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Очікується JSON-тіло запиту"}), 400

    product_id = data.get("product_id")
    status = data.get("status", "Нове")

    if not isinstance(product_id, int) or isinstance(product_id, bool):
        return jsonify({"error": "Некоректне значення product_id"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO orders (product_id, status) VALUES (?, ?)",
        (product_id, status),
    )
    db.commit()

    created = db.execute(
        "SELECT * FROM orders WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify({"api_version": "v2", "order": dict(created)}), 201