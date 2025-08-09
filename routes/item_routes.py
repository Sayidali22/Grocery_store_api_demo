from flask import Blueprint, request, jsonify
from models import User, Item, CartItem
from extensions import db

item_bp = Blueprint('item', __name__, url_prefix='/items')

# GET /items - fetch all items
@item_bp.route('', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([
        {"id": item.id, "name": item.name, "price": float(item.price)}
        for item in items
    ])

# POST /items - add a new item
@item_bp.route('', methods=['POST'])
def add_items():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({"error": "Missing name or price"}), 400

    new_item = Item(name=name, price=price)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item added", "id": new_item.id}), 201
