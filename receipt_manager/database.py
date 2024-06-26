from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Receipt(db.Model):
    """
    Represents a receipt in the database.

    Attributes:
        id (int): The unique identifier of the receipt.
        date (str): The date of the receipt.
        company (str): The name of the company associated with the receipt.
        price (float): The total price of the receipt.
        products (list): A list of products associated with the receipt.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    company = db.Column(db.String(50))
    price = db.Column(db.Float)
    products = db.relationship('Product', backref='receipt', lazy=True)

class Product(db.Model):
    """
    Represents a product in the receipt manager.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        quantity (int): The quantity of the product.
        receipt_id (int): The ID of the receipt that this product belongs to.
        
    Relationships:
        - Each product belongs to a single receipt.
        - Each receipt can have multiple products.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
