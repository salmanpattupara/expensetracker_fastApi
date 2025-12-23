from typing import Annotated
from fastapi import FastAPI,routing,HTTPException,Depends
from database import SessionLocal,engine
from sqlalchemy.orm import Session
import category.models as models
from category.category import router as category_router
from transaction.transactions import router as transaction_router



app=FastAPI()
models.Base.metadata.create_all(bind=engine)







app.include_router(category_router)
app.include_router(transaction_router)
#app.include_router(notes_router)
    