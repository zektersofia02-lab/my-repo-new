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