from typing import Annotated
from fastapi import APIRouter, Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from category.models import Category  as category_model
from category.models import User_category as user_category
import category.schemas as schemas
from database import get_db
from user.service import get_current_user



router=APIRouter(
    prefix="/category", tags=["category"]
)

user_dependency=Annotated[dict,Depends(get_current_user)]


#categories
@router.get("/")
async def all_categories(current_user = Depends(get_current_user),db:Session=Depends(get_db),):
    print(current_user['id'])
    if current_user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        all_category=db.query(user_category).filter(user_category.user_id==current_user['id']).all()
        #all_category=db.query(category_model).all()
        if not all_category:
            return HTTPException(status_code=404,detail="No categories found")
        return all_category
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured- {e}")

#individual category
@router.get("/{id}",response_model=schemas.CategoryResponse)     
async def get_category(id:int,db:Session=Depends(get_db),):
    try: 
        result=db.query(category_model.Category).filter(category_model.Category.id==id).first()
        if not result:
            return HTTPException(status_code=404,detail="category not found")
        
        return result
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#add new category
@router.post("/")
async def add_category(category:schemas.CategoryBase,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        category_name = category.name.lower()
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
async def update_category(id:int,category:schemas.CategoryBase,db:Session=Depends(get_db)):
    try:
        result=db.query(user_category).filter(user_category.category_id==id).first()
        if not result:
            return HTTPException(status_code=404,detail="category not found")
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
async def delete_category(id:int,db:Session=Depends(get_db)):
    try:
        db_cat=db.query(models.Category).filter(models.Category.id==id).first()
        if not db_cat:
            return HTTPException(status_code=404,detail="category not found")
        db.delete(db_cat)
        db.commit()
        return {"message":"deleted successfully "}
        
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
        