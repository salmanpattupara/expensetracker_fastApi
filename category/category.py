from fastapi import APIRouter, Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
import category.models as models
import category.schemas as schemas
from database import get_db



router=APIRouter(
    prefix="/category", tags=["category"]
)

#categories
@router.get("/")
async def all_categories(db:Session=Depends(get_db)):
    try:
        all_category=db.query(models.Category).all()
        if not all_category:
            return HTTPException(status_code=404,detail="category not found")
        return all_category
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#individual category
@router.get("/{id}",response_model=schemas.CategoryResponse)     
async def get_category(id:int,db:Session=Depends(get_db)):
    try: 
        result=db.query(models.Category).filter(models.Category.id==id).first()
        if not result:
            return HTTPException(status_code=404,detail="category not found")
        
        return result
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#aiop add new category
@router.post("/")
async def add_category(category:schemas.CategoryBase,db:Session=Depends(get_db)):
    try:
        db_categories=models.Category(name=category.name.lower(),budget=category.budget)
        db.add(db_categories)
        try:
            db.commit()
            db.refresh(db_categories)
            return db_categories  
        except Exception as e:
            return HTTPException(status_code=500,detail=f"Category already exist")
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#update category name
@router.put("/{id}")
async def update_category(id:int,category:schemas.CategoryBase,db:Session=Depends(get_db)):
    try:
        result=db.query(models.Category).filter(models.Category.id==id).first()
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
async def delete_category(id:int,category:schemas.CategoryBase,db:Session=Depends(get_db)):
    try:
        db_cat=db.query(models.Category).filter(models.Category.id==id).first()
        if not db_cat:
            return HTTPException(status_code=404,detail="category not found")
        db.delete(db_cat)
        db.commit()
        return {"message":"deleted successfully "}
        
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
        