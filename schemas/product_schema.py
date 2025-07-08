from flask_marshmallow import Marshmallow
from models.product import Product

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)