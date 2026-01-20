from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as SQLEnum, Date,DateTime
from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy.orm import relationship
from api.category_api.models import Category
from api.database import Base




class TransactionType(PyEnum):
	EXPENSE = "expense"
	INCOME = "income"



class Transaction(Base):
	__tablename__ = "transactions"

	id = Column(Integer, primary_key=True, index=True)
	user_id=Column(Integer,ForeignKey("users.id"))
	description = Column(String, nullable=True)
	amount = Column(Integer, nullable=False)
	type = Column(SQLEnum(TransactionType, name="transaction_type"), nullable=False)
	category_id=Column(Integer,ForeignKey("user_category",ondelete="SET NULL"),nullable=True)
	date = Column(Date, nullable=False)
	created_at = Column(DateTime, default=datetime.now, nullable=False)
	updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
 
 
	user_category = relationship("User_category", back_populates="transactions")
	user = relationship("User", back_populates="transactions")

 
	
 