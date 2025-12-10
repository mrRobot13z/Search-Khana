# db.py

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Item(db.Model):
    # Sets the table name in the database 
    __tablename__ = 'items'

    # Columns: [id, barcode, name, cost, sell]
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    sell = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.barcode}')"