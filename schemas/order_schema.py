from flask_marshmallow import Marshmallow
from models.order import Order
from schemas.user_schema import UserSchema
from schemas.product_schema import ProductSchema
from marshmallow import fields

ma = Marshmallow()

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

order_schema = OrderSchema()
orders_schema = OrderSchema(many = True)
