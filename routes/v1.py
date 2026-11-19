from flask import Blueprint, jsonify, request
from models import get_db

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


# --- Товари / послуги (products) ---

@api_v1.route("/products", methods=["GET"])
def get_products_v1():
    rows = get_db().execute("SELECT * FROM products").fetchall()
    return jsonify([dict(row) for row in rows]), 200


@api_v1.route("/products/<int:product_id>", methods=["GET"])
def get_product_v1(product_id):
    row = get_db().execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return jsonify(dict(row)), 200


@api_v1.route("/products", methods=["POST"])
def create_product_v1():
    data = request.get_json(silent=True)
    if not data or not data.get("title") or not isinstance(data.get("price"), (int, float)):
        return jsonify({"error": "Потрібні поля title (рядок) і price (число)"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO products (title, price, description) VALUES (?, ?, ?)",
        (data["title"], data["price"], data.get("description", "")),
    )
    db.commit()
    return jsonify({
        "id": cursor.lastrowid,
        "title": data["title"],
        "price": data["price"],
        "description": data.get("description", ""),
    }), 201


@api_v1.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product_v1(product_id):
    db = get_db()
    cursor = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Послугу/товар не знайдено"}), 404
    return "", 204


# --- Замовлення (orders) ---

@api_v1.route("/orders", methods=["GET"])
def get_orders_v1():
    rows = get_db().execute("SELECT * FROM orders").fetchall()
    return jsonify([dict(row) for row in rows]), 200


@api_v1.route("/orders", methods=["POST"])
def create_order_v1():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("product_id"), int):
        return jsonify({"error": "Потрібне поле product_id (ціле число)"}), 400

    db = get_db()
    product = db.execute(
        "SELECT id FROM products WHERE id = ?", (data["product_id"],)
    ).fetchone()
    if product is None:
        return jsonify({"error": "Вказаний товар/послуга не існує"}), 404

    status = data.get("status", "Новий")
    cursor = db.execute(
        "INSERT INTO orders (product_id, status) VALUES (?, ?)",
        (data["product_id"], status),
    )
    db.commit()
    return jsonify({
        "id": cursor.lastrowid,
        "product_id": data["product_id"],
        "status": status,
    }), 201