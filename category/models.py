from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy.orm import relationship

 
class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,unique=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    user_category=relationship("User_category", back_populates="category")
   

class User_category(Base):
    
    __tablename__="user_category"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    category_id=Column(Integer,ForeignKey("category.id"))
    budget=Column(Integer,nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
     
    transactions = relationship("Transaction", back_populates="user_category")
    user = relationship("User", back_populates="user_category")
    category = relationship("Category", back_populates="user_category")


    
   