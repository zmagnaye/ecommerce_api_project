from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.base import Base
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

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many = True)
product_schema = ProductSchema()
product_schema = ProductSchema(many = True)
order_schema = OrderSchema()
order_schema = OrderSchema(many = True)

if __name__ == "__main__":
    with app.app_context():
        print("base.metadata") 
        from models.base import Base
        Base.metadata.create_all(db.engine)
        # db.create_all()
        print("tables created") 

    app.run(debug=True)