from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime



 
class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,unique=True)
    budget=Column(Integer,nullable=True)
    
    transactions = relationship("Transaction", back_populates="category")
    
    