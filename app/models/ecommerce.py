from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    name: Mapped[str] = mapped_column(index=True)
    
    description: Mapped[str] = mapped_column() 
    
    price: Mapped[float] = mapped_column()
    
    stock: Mapped[int] = mapped_column(default=0)
    
    attributes: Mapped[dict[str, Any]] = mapped_column(JSON, default={}) 
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    user_email: Mapped[str] = mapped_column(index=True)
    
    status: Mapped[str] = mapped_column(default="pending") 
    
    total_amount: Mapped[float] = mapped_column(default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())