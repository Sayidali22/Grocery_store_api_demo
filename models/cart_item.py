from extensions import db

class CartItem(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
     quantity = db.Column(db.Integer, nullable=False)