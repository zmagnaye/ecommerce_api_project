from sqlalchemy import Table, Column, ForeignKey
from config import db

# Association Table
order_product = Table(
    "order_product",
    db.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key = True),
    Column("product_id", ForeignKey("products.id"), primary_key = True)
)