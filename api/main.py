from typing import Annotated
from fastapi import FastAPI,routing,HTTPException,Depends
from api.database import engine
from sqlalchemy.orm import Session
from api.category_api import models as models
from api.category_api.category import router as category_router
from api.transaction_api.transactions import router as transaction_router
from api.analyze.analysis import router as analytics_router
from api.user_api.user import router as user_router



app=FastAPI(title="Expense Tracker API",description="An API to track your expenses and income",version="1.0.0")

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(analytics_router)

#app.include_router(notes_router)
    