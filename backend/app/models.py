from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(20), nullable=False)
    is_income = Column(Boolean, default=False)
    icon = Column(String(50), nullable=True)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, server_default=func.now())
    is_income = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
