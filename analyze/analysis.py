from calendar import monthrange
from datetime import date, datetime, timedelta
from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from transaction.models import Transaction as transaction_models
from category.models import Category as category_models
import category.schemas as schemas
from database import get_db



router=APIRouter(
    prefix="/analytics", tags=["analytics"]
)



   
#sum of transaction in a month
@router.get("/day/total")
def get_day_total(
     date_: date = Query(..., alias="date", example="2025-01-20"),
    db:Session=Depends(get_db)):
    
    start_datetime = datetime.combine(date_, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)
  
    try:
        results = (
            db.query(
                category_models.name.label("category"),
                func.sum(transaction_models.amount).label("amount"),
            )
            .join(transaction_models, transaction_models.category_id == category_models.id)
            .filter(
                #transaction_models.transaction.user_id == current_user.id,
                transaction_models.created_at >= start_datetime,
                transaction_models.created_at <= end_datetime,
            )
            .group_by(category_models.name)
            .all()
        )

        categories = [
            {"category": row.category, "amount": row.amount}
            for row in results
        ]

        total_amount = sum(row["amount"] for row in categories)
        
        
        if not total_amount:
            return HTTPException(status_code=200,detail="no transaction")
        return {
            "status" : 200,
             "date": date_,
             "total_amount": total_amount,
            "categories": categories
        }
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
   
#sum of transaction in a month,inclduding category-wise breakdown
@router.get("/month/total")
def get_monthly_total(
    year: int = Query(..., example=2025),
    month: int = Query(..., ge=1, le=12),
    db:Session=Depends(get_db)):
    
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)
  
    try:

        # total_amount = (
        # db.query(func.coalesce(func.sum(transaction_models.Transaction.amount), 0))
        # .filter(
        #     transaction_models.Transaction.created_at >= start_date,
        #     transaction_models.Transaction.created_at <= end_date,
        # ).scalar())
        results = (
            db.query(
                category_models.name.label("category"),
                func.sum(transaction_models.amount).label("amount"),
            )
            .join(transaction_models, transaction_models.category_id == category_models.id)
            .filter(
                #transaction_models.transaction.user_id == current_user.id,
                transaction_models.created_at >= start_date,
                transaction_models.created_at <= end_date,
            )
            .group_by(category_models.name)
            .all()
        )

        categories = [
            {"category": row.category, "amount": row.amount}
            for row in results
        ]

        total_amount = sum(row["amount"] for row in categories)
        
        
        if not total_amount:
            return HTTPException(status_code=200,detail="no transaction")
        return {
            "status" : 200,
             "year": year,
             "month": month,
             "total_amount": total_amount,
            "categories": categories
        }
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    

#total of transaction per year 
@router.get("/year/total")
def get_yearly_total(
    year: int = Query(..., example=2025),
    db:Session=Depends(get_db)):
    
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
  
    try:
        results = (
            db.query(
                category_models.name.label("category"),
                func.sum(transaction_models.amount).label("amount"),
            )
            .join(transaction_models, transaction_models.category_id == category_models.id)
            .filter(
                #transaction_models.transaction.user_id == current_user.id,
                transaction_models.date >= start_date,
                transaction_models.date <= end_date,
            )
            .group_by(category_models.name)
            .all()
        )

        categories = [
            {"category": row.category, "amount": row.amount}
            for row in results
        ]

        total_amount = sum(row["amount"] for row in categories)
        
        
        if not total_amount:
            return HTTPException(status_code=200,detail="no transaction")
        return {
            "status" : 200,
             "year": year,
           
             "total_amount": total_amount,
            "categories": categories
        }
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")