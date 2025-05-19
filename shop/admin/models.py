from shop import db
from datetime import datetime

# User table (table for the SecureCart users)
class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Admin table (table for the SecureCart admins)
class Admin(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"

# Product table (table for SecureCart's products)
class Product(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}, Price {self.price}>"

# Order table (this table stores customer's complete orders)
class Order(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # this is a foreign key in the User table

    user = db.relationship('User', backref='orders', lazy=True)  # links Order to User

    def __repr__(self):
        return f"<Order {self.id}, User {self.user_id}, Total {self.total_price}>"

# OrderItem table (this table stores the items that the customer ordered)
class OrderItem(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', backref='items', lazy=True)  # links OrderItem to Order
    product = db.relationship('Product', backref='order_items', lazy=True)  # links OrderItem to Product

    def __repr__(self):
        return f"<OrderItem Order {self.order_id}, Product {self.product_id}, Quantity {self.quantity}>"