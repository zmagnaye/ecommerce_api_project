from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey
from datetime import datetime
from typing import List
from config import db
from .order_product import order_product

class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key = True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates = "orders")
    products: Mapped[List["Product"]] = relationship("Product", secondary = "order_product", back_populates = "orders")