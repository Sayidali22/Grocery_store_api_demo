from .auth_routes import auth_bp
from .item_routes import item_bp
from .cart_routes import cart_bp

all_blueprints = [auth_bp, item_bp, cart_bp]
