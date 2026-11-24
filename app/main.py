"""Demo E-Commerce Application - Flask backend for UI automation testing."""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


# ---------------------------------------------------------------------------
# In-memory data store (for demonstration purposes only)
# ---------------------------------------------------------------------------
PRODUCTS: List[dict] = [
    {
        "id": 1,
        "name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "price": 79.99,
        "description": "Premium over-ear wireless headphones with active noise cancellation and 30-hour battery life.",
        "image": "/static/images/headphones.jpg",
        "stock": 50,
        "rating": 4.7,
        "reviews": 128,
    },
    {
        "id": 2,
        "name": "Smartphone Case - Protective Shell",
        "category": "Accessories",
        "price": 24.99,
        "description": "Shock-absorbent protective case with raised edges for screen protection.",
        "image": "/static/images/case.jpg",
        "stock": 120,
        "rating": 4.5,
        "reviews": 245,
    },
    {
        "id": 3,
        "name": "Stainless Steel Water Bottle",
        "category": "Home & Kitchen",
        "price": 32.50,
        "description": "Insulated stainless steel water bottle keeps drinks cold for 24 hours or hot for 12 hours.",
        "image": "/static/images/bottle.jpg",
        "stock": 85,
        "rating": 4.8,
        "reviews": 312,
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "price": 119.99,
        "description": "Compact mechanical keyboard with blue switches, RGB backlighting, and programmable keys.",
        "image": "/static/images/keyboard.jpg",
        "stock": 35,
        "rating": 4.9,
        "reviews": 189,
    },
    {
        "id": 5,
        "name": "Running Shoes - Air Cushion",
        "category": "Sports",
        "price": 89.99,
        "description": "Lightweight running shoes with air-cushion soles for maximum comfort and performance.",
        "image": "/static/images/shoes.jpg",
        "stock": 60,
        "rating": 4.6,
        "reviews": 203,
    },
    {
        "id": 6,
        "name": "Webcam 1080p",
        "category": "Electronics",
        "price": 59.99,
        "description": "Full HD 1080p webcam with built-in microphone and privacy shutter.",
        "image": "/static/images/webcam.jpg",
        "stock": 45,
        "rating": 4.4,
        "reviews": 156,
    },
    {
        "id": 7,
        "name": "Laptop Stand - Aluminum",
        "category": "Home & Kitchen",
        "price": 45.00,
        "description": "Ergonomic aluminum laptop stand with adjustable height and ventilation design.",
        "image": "/static/images/stand.jpg",
        "stock": 70,
        "rating": 4.6,
        "reviews": 178,
    },
    {
        "id": 8,
        "name": "Coffee Maker - Programmable",
        "category": "Home & Kitchen",
        "price": 69.99,
        "description": "Programmable coffee maker with 12-cup capacity and auto-shutoff feature.",
        "image": "/static/images/coffee.jpg",
        "stock": 25,
        "rating": 4.7,
        "reviews": 134,
    },
    {
        "id": 9,
        "name": "Yoga Mat - Non-Slip",
        "category": "Sports",
        "price": 29.99,
        "description": "Extra-thick non-slip yoga mat with alignment lines and carrying strap.",
        "image": "/static/images/yoga.jpg",
        "stock": 90,
        "rating": 4.5,
        "reviews": 267,
    },
    {
        "id": 10,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 199.99,
        "description": "Smart watch with heart rate monitoring, GPS, and 7-day battery life.",
        "image": "/static/images/watch.jpg",
        "stock": 40,
        "rating": 4.8,
        "reviews": 192,
    },
]

USERS: Dict[str, dict] = {}
ORDERS: List[dict] = []


def get_product(product_id: int) -> Optional[dict]:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def search_products(query: str) -> List[dict]:
    q = query.lower()
    return [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower()]


def filter_products(category: Optional[str] = None) -> List[dict]:
    if category:
        return [p for p in PRODUCTS if p["category"].lower() == category.lower()]
    return PRODUCTS


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    q = request.args.get("q", "")
    category = request.args.get("category", "")
    products = filter_products(category)
    if q:
        products = [p for p in products if q in p["name"].lower() or q in p["category"].lower()]
    categories = sorted(set(p["category"] for p in PRODUCTS))
    cart = session.get("cart", {})
    cart_count = sum(item["quantity"] for item in cart.values())
    return render_template(
        "index.html",
        products=products,
        categories=categories,
        cart_count=cart_count,
        query=q,
        selected_category=category,
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id: int):
    product = get_product(product_id)
    if not product:
        return render_template("404.html"), 404
    cart = session.get("cart", {})
    cart_count = sum(item["quantity"] for item in cart.values())
    return render_template("product.html", product=product, cart_count=cart_count)


@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0.0
    for pid_str, item in cart.items():
        product = get_product(int(pid_str))
        if product:
            subtotal = product["price"] * item["quantity"]
            cart_items.append({**product, "quantity": item["quantity"], "subtotal": subtotal})
            total += subtotal
    cart_count = sum(i["quantity"] for i in cart.values())
    return render_template("cart.html", cart_items=cart_items, total=total, cart_count=cart_count)


@app.route("/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json(silent=True) or request.form
    product_id = int(data.get("product_id"))
    quantity = int(data.get("quantity", 1))
    product = get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    cart = session.get("cart", {})
    pid_str = str(product_id)
    if pid_str in cart:
        cart[pid_str]["quantity"] += quantity
    else:
        cart[pid_str] = {"quantity": quantity}
    session["cart"] = cart
    cart_count = sum(i["quantity"] for i in cart.values())
    return jsonify({"success": True, "cart_count": cart_count, "product": product["name"]})


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    data = request.get_json(silent=True) or request.form
    pid_str = str(int(data.get("product_id")))
    cart = session.get("cart", {})
    cart.pop(pid_str, None)
    session["cart"] = cart
    cart_count = sum(i["quantity"] for i in cart.values())
    return jsonify({"success": True, "cart_count": cart_count})


@app.route("/cart/update", methods=["POST"])
def cart_update():
    data = request.get_json(silent=True) or request.form
    pid_str = str(int(data.get("product_id")))
    quantity = int(data.get("quantity", 1))
    cart = session.get("cart", {})
    if quantity <= 0:
        cart.pop(pid_str, None)
    else:
        cart[pid_str] = {"quantity": quantity}
    session["cart"] = cart
    cart_count = sum(i["quantity"] for i in cart.values())
    return jsonify({"success": True, "cart_count": cart_count})


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("index"))

    if request.method == "POST":
        order_id = str(uuid.uuid4())[:8].upper()
        cart_items = []
        total = 0.0
        for pid_str, item in cart.items():
            product = get_product(int(pid_str))
            if product:
                subtotal = product["price"] * item["quantity"]
                cart_items.append({**product, "quantity": item["quantity"], "subtotal": subtotal})
                total += subtotal

        order = {
            "order_id": order_id,
            "items": cart_items,
            "total": total,
            "status": "confirmed",
            "created_at": datetime.utcnow().isoformat(),
            "customer": {
                "name": request.form.get("customer_name", ""),
                "email": request.form.get("customer_email", ""),
                "address": request.form.get("customer_address", ""),
            },
        }
        ORDERS.append(order)
        session.pop("cart", None)
        return render_template("order_confirmation.html", order=order)

    cart_items = []
    total = 0.0
    for pid_str, item in cart.items():
        product = get_product(int(pid_str))
        if product:
            subtotal = product["price"] * item["quantity"]
            cart_items.append({**product, "quantity": item["quantity"], "subtotal": subtotal})
            total += subtotal
    cart_count = sum(i["quantity"] for i in cart.values())
    return render_template("checkout.html", cart_items=cart_items, total=total, cart_count=cart_count)


@app.route("/orders/<order_id>")
def order_detail(order_id: str):
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        return render_template("404.html"), 404
    return render_template("order_detail.html", order=order)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        user = USERS.get(email)
        if user and user["password"] == password:
            session["user_email"] = email
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if email in USERS:
            return render_template("register.html", error="Email already registered")
        USERS[email] = {"name": name, "email": email, "password": password}
        session["user_email"] = email
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("index"))


@app.route("/orders")
def order_history():
    user_email = session.get("user_email")
    if not user_email:
        return redirect(url_for("login"))
    user_orders = [o for o in ORDERS if o["customer"]["email"] == user_email]
    return render_template("order_history.html", orders=user_orders)


@app.route("/api/products")
def api_products():
    return jsonify(PRODUCTS)


@app.route("/api/products/<int:product_id>")
def api_product(product_id: int):
    product = get_product(product_id)
    if not product:
        return jsonify({"error": "Not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
