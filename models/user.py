from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from config import db

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    address: Mapped[str] = mapped_column(String(200), nullable = False)
    email: Mapped[str] = mapped_column(String(100), nullable = False, unique = True)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates = "user")