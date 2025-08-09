from flask import Flask, jsonify, request
from config import Config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256
from extensions import db, migrate
from routes import all_blueprints
from models import User, Item, CartItem

for bp in all_blueprints:
    app.register_blueprint(bp)

# Create the flask app 
app = Flask(__name__)

# Load the config from your Config class
app.config.from_object(Config)

# Set up JWT manager to handle token creation and verification used for authentication
jwt = JWTManager(app)

# Initialize extensions here!
db.init_app(app)
migrate.init_app(app, db)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized"}), 401

# Basic route just to test the app works
@app.route('/')
def home():
    return 'Flask is connected to the database!' 

if __name__ == '__main__':
    app.run(debug=True)