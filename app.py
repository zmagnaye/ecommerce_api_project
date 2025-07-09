from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import select
from config import db, ma
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


if __name__ == "__main__":
    with app.app_context():
        print("base.metadata") 
        from models.base import Base
        Base.metadata.create_all(db.engine)
        # db.create_all()
        print("tables created") 

    app.run(debug=True)