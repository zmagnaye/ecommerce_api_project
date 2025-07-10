from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import select
from config import db, ma
from datetime import datetime
# from models.base import Base
from models.user import User
from models.product import Product
from models.order import Order
from models.order import order_product
from schemas.user_schema import UserSchema
from schemas.product_schema import ProductSchema
from schemas.order_schema import OrderSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many = True)
product_schema = ProductSchema()
products_schema = ProductSchema(many = True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many = True)

# Routes
# Create New Users
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    existing_user = User.query.filter_by(email = user_data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email already exists!"}), 409

    new_user = User(name = user_data["name"], email = user_data["email"], address = user_data["address"])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

# Fetch All Users
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200

# Fetch a Single User by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return user_schema.jsonify(user), 200

# Update a User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    if user_data["email"] != user.email:
        existing_user = db.session.execute(select(User).filter_by(email = user_data["email"])).scalars().first()
        if existing_user:
            return jsonify({"error": "Email already exists!"}), 409

    user.name = user_data['name']
    user.email = user_data['email']
    user.address = user_data['address']

    db.session.commit()
    return user_schema.jsonify(user), 200

# Delete a User
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"succefully deleted user {id}"}), 200

# Create a Product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name = product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

# Get all Products
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()

    return products_schema.jsonify(products), 200

# Get Products by ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    query = select(id).where(Product.id == id)
    product = db.session.get(Product, id)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return product_schema.jsonify(product), 200

# Update a Product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Product not Found"}), 400
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']

    db.session.commit()
    return product_schema.jsonify(product), 200

# Delete a Product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"succefully deleted product {id}"}), 200

# Create Order
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json

    user_id = order_data.get("user_id")
    order_date = order_data.get("order_date")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
        
    if order_date:
        try:
            order_date = datetime.strptime(order_date, "%Y-%m-%d")
        except ValueError:
           return jsonify({"error": "Order Date must be in YYYY-MM-DD format"}), 400
    else:
        order_date = datetime.utcnow()
       
    new_order = Order(user_id = user_id, order_date = order_date)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201

# Add a Product to an Order (Duplicate Prevention)
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order or not product:
        return jsonify({"error": "Order or Product not found."}), 400
    
    # Avoid duplicates
    if product in order.products:
        return jsonify({"error": "Product already in order."}), 400
    
    order.products.append(product)
    db.session.commit()

    return jsonify({"message": f"Product {product.product_name} added to order {order_id}"}), 200

# Remove a Product from Order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order or not product:
        return jsonify({"error": "Order or Product not found."}), 400
    
    if product not in order.products:
        return jsonify({"error": "Product not in order."}), 400
    
    order.products.remove(product)
    db.session.commit()

    return jsonify({"message": f"Product {product.product_name} removed to order {order_id}"}), 200

# Get all orders from user
@app.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found."}), 400
    return orders_schema.jsonify(user.orders), 200

# Get all products from an order

if __name__ == "__main__":
    with app.app_context():
        print("base.metadata") 
        from models.base import Base
        Base.metadata.create_all(db.engine)
        # db.create_all()

    app.run(debug=True)
