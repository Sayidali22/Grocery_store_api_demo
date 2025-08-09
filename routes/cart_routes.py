from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Item, CartItem
from extensions import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# GET /cart - view current user's cart
@cart_bp.route('', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()
    cart_items = db.session.query(CartItem, Item).join(Item, CartItem.item_id == Item.id).filter(CartItem.user_id == user_id).all()

    cart_data = []
    total = 0

    for cart_item, item in cart_items:
        subtotal = cart_item.quantity * item.price
        cart_data.append({
            "item_id": item.id,
            "name": item.name,
            "price": float(item.price),
            "quantity": cart_item.quantity,
            "subtotal": float(subtotal)
        })

        total += subtotal

    return jsonify({"cart": cart_data, "total": float(total)})


# POST /cart - add item to cart
@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    user_id = get_jwt_identity()

    if not item_id or not quantity:
        return jsonify({"error": "item_id and quantity are required"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    if not Item.query.get(item_id):
        return jsonify({"error": "Item not found"}), 404

    cart_item = CartItem.query.filter_by(user_id=user_id, item_id=item_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart."}), 201


# DELETE /cart/<item_id> - remove item from cart
@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_from_cart(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(user_id=user_id, item_id=item_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item has been deleted from cart."})
    else:
        return jsonify({"error": "Item was not found in cart."}), 404
