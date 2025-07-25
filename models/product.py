from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float
from typing import List
from config import db
from models.order_product import order_product

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key = True)
    product_name: Mapped[str] = mapped_column(String(100), nullable = False)
    price: Mapped[float] = mapped_column(Float, nullable = False)

    orders: Mapped[List["Order"]] = relationship("Order", secondary = "order_product", back_populates = "products")