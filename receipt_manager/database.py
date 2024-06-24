from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receipts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    company = db.Column(db.String(50))
    price = db.Column(db.Float)
    products = db.relationship('Product', backref='receipt', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
