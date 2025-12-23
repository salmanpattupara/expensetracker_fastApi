from pydantic import BaseModel, field_validator
from datetime import date
from transaction.models import TransactionType
from typing import Optional


class TransactionBase(BaseModel):
    amount:int
    type:TransactionType
    description:str
    date:date #user input date
    category_id:Optional[int]

    
class TransactionCreate(TransactionBase):

    
    @field_validator("date")
    @classmethod
    def no_future_dates(cls, v):
        if v > date.today():
            raise ValueError("Transaction date cannot be in the future")
        return v
# class TransactionResponse(TransactionBase):
   

#     class Config:
#         orm_mode = True