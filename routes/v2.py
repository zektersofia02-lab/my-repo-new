from flask import Blueprint, jsonify, request
from models import get_db

api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")


@api_v2.route("/products", methods=["GET"])
def get_products_v2():
    rows = get_db().execute("SELECT * FROM products").fetchall()
    products = [dict(row) for row in rows]
    return jsonify({
        "api_version": "v2",
        "count": len(products),
        "products": products,
    }), 200


@api_v2.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product_v2(product_id):
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
    db = get_db()
    cursor = db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Замовлення не знайдено"}), 404
    return "", 204
@api_v2.route("/products/<int:product_id>", methods=["GET"])
def get_product_v2(product_id):
    row = get_db().execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return jsonify({"api_version": "v2", "product": dict(row)}), 200


@api_v2.route("/products", methods=["POST"])
def create_product_v2():
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
    db = get_db()
    cursor = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return "", 204


@api_v2.route("/orders", methods=["GET"])
def get_orders_v2():
    rows = get_db().execute("SELECT * FROM orders").fetchall()
    orders = [dict(row) for row in rows]
    return jsonify({
        "api_version": "v2",
        "count": len(orders),
        "orders": orders,
    }), 200


@api_v2.route("/orders/<int:order_id>", methods=["GET"])
def get_order_v2(order_id):
    row = get_db().execute(
        "SELECT * FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Замовлення не знайдено"}), 404
    return jsonify({"api_version": "v2", "order": dict(row)}), 200


@api_v2.route("/orders", methods=["POST"])
def create_order_v2():
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