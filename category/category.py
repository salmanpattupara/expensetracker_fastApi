from calendar import monthrange
from datetime import datetime,date, timedelta
from typing import Annotated
from fastapi import APIRouter, Response,status,HTTPException,Depends,Query
from sqlalchemy import extract
from sqlalchemy.orm import Session
from category.models import Category  as category_model
from category.models import User_category as user_category
from transaction import models as models
import category.schemas as schemas
import transaction.schemas as t_schemas
from database import get_db
from user.service import get_current_user
from sqlalchemy.exc import SQLAlchemyError



router=APIRouter(
    prefix="/category", tags=["category"]
)

user_dependency=Annotated[dict,Depends(get_current_user)]


#categories
@router.get("/",response_model=list[schemas.User_categoryResponse])
async def all_categories(current_user = Depends(get_current_user),db:Session=Depends(get_db),):
   
    if current_user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        all_category=db.query(user_category).filter(user_category.user_id==current_user['id']).all()
       
        if not all_category:
            raise HTTPException(status_code=404,detail="No categories found")
        return all_category
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"some error occured- {e}")

#individual category
@router.get("/{id}",response_model=schemas.User_categoryResponse)     
async def get_category(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    if current_user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try: 
        result=db.query(user_category).filter(user_category.id==id,user_category.user_id==current_user['id']).first()
       
        if not result:
            raise HTTPException(status_code=404,detail="category not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"some error occured {e}")

#add new category
@router.post("/")
async def add_category(category:schemas.User_categoryBase,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
    print("safayrtaysdy")
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        print("`sdfsa")
        category_name = category.name.lower()
        print("category name:", category_name  )
        category_exists = db.query(category_model).filter(category_model.name == category_name).first()
        
        #check if category exists
        if not category_exists:
            new_category = category_model(name=category_name)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            category_exists = new_category
        
        #check if user_category exists or not
        user_cat_exists = db.query(user_category).filter(
            user_category.category_id == category_exists.id,
            user_category.user_id == current_user['id']
        ).first()
        
        #raise exception if exists
        if user_cat_exists:
            raise HTTPException(status_code=400, detail="Category already exists for this user")
        
        #add to user category if not exists 
        db_user_category = user_category(
            category_id=category_exists.id,
            budget=category.budget,
            user_id=current_user['id']
        )
        db.add(db_user_category)
        db.commit()
        db.refresh(db_user_category)
        return db_user_category
        
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured")

#update category name
@router.put("/{id}")
async def update_category(id:int,category:schemas.User_categoryBase,db:Session=Depends(get_db),
                          current_user = Depends(get_current_user)):
    try:
        result=db.query(user_category).filter(user_category.category_id==id).first()
        
        if not result:
            return HTTPException(status_code=404,detail="category not found")
        if result.user_id != current_user['id']:
            return HTTPException(status_code=403,detail="forbidden action")
        result.name=category.name
        result.budget=category.budget
        try:
            db.commit()
            db.refresh(result)
            return result 
        except Exception as e:
            return HTTPException(status_code=500,detail=f"Category already exist")
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
      
#delete category
@router.delete("/{id}",status_code=200)
async def delete_category(id:int,db:Session=Depends(get_db),
                          current_user = Depends(get_current_user)):
    try:
        result=db.query(user_category).filter(user_category.category_id==id).first()
        
        if not result:
            return HTTPException(status_code=404,detail="category not found")
        if result.user_id != current_user['id']:
            return HTTPException(status_code=403,detail="forbidden action")
        if not result:
            return HTTPException(status_code=404,detail="category not found")
        db.delete(result)
        db.commit()
        return {"message":"deleted successfully "}
        
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    
    
@router.get("/{id}/transactions",response_model=list[t_schemas.TransactionResponse])
async def category_wise_transactions(id:int, 
        year: int = Query(..., example=2025),
        month: int = Query(..., ge=1, le=12),
        current_user = Depends(get_current_user),
        db:Session=Depends(get_db)):
    
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)
    
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
   
    category = (
        db.query(user_category)
        .filter(
            user_category.category_id == id,
            user_category.user_id == current_user['id']
        )
        .first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
        
    try:
        result=db.query(models.Transaction).filter(
            models.Transaction.user_id==current_user['id'],
            models.Transaction.category_id==id,
              models.Transaction.created_at >= start_date,
            extract("year",  models.Transaction.created_at)==year,
            extract("month", models.Transaction.created_at) == month)
        if not result:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="no transactions found for this category")
        return result
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error occurred"
        )
        