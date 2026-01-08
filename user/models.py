from sqlalchemy import Column, Integer, String,Boolean
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    user_category = relationship("User_category", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    
    