from calendar import monthrange
from datetime import datetime,date, timedelta
from fastapi import APIRouter, Query, Response,status,HTTPException,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
import transaction.models as models
import transaction.schemas as schemas
from database import get_db
from user.service import get_current_user


#router
router=APIRouter(
    prefix="/transaction", tags=["transaction"]
)


#get transaction 
@router.get("/",status_code=status.HTTP_200_OK,response_model=list[schemas.TransactionResponse])
async def transactions(db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
   
    try:
        result=db.query(models.Transaction).filter(models.Transaction.user_id==current_user['id']).all()
        if not result:
            return HTTPException(status_code=200,detail="no transaction")
        return result
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    

#add new transaction
@router.post("/")
async def new_transaction(transaction:schemas.TransactionCreate,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        transaction_data=transaction.model_dump()
        transaction_data['user_id']=current_user['id']
        db_txn=models.Transaction(**transaction_data)
        db.add(db_txn)
        try:
            db.commit()
            db.refresh(db_txn)
            return db_txn
        except:
            return HTTPException(status_code=500,detail="something went wrong")
        # if not result:
        #     return HTTPException(status_code=200,detail="no transaction")
        # return result
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#individual transaction 
@router.get("/{id}")
async def get_transaction(id:int,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        result=db.query(models.Transaction).filter(models.Transaction.id==id,models.Transaction.user_id==current_user['id']).first()
        if not result:
            return HTTPException(status_code=404,detail="not found")
        return result
    except Exception as e:
        return HTTPException(status_code=400,detail=f"bad request")
    
#edit transaction
@router.put("/{id}")
async def edit_transaction(id:int,transaction:schemas.TrasactionUpdate,current_user = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user")
    try:
        result=db.query(models.Transaction).filter(models.Transaction.id==id,models.Transaction.user_id==current_user['id']).first()
        if not result:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="not found")
        update_data=transaction.model_dump(exclude_unset=True)
        for field,value in update_data.items():
            setattr(result,field,value)
        try:
            db.commit()
            db.refresh(result)
            return result
        except:
            return HTTPException(status_code=500,detail="something went wrong")
        

    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")

#delete transaction
@router.delete("/{id}")
async def delete_transaction(id:int,db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    try:
        result=db.query(models.Transaction).filter(models.Transaction.id==id).first()
        
        if not result:
            return HTTPException(status_code=404,detail="not found")
        if not result.user_id==current_user['id']:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not Authorized")
        db.delete(result)
        db.commit()
        return {"message":"deleted successfully "}
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
        
    
#transactions per month
@router.get("/month/all",status_code=status.HTTP_200_OK)
async def get_monthly_transactions(
    year: int = Query(..., example=2025),
    month: int = Query(..., ge=1, le=12),
    db:Session=Depends(get_db)):
    
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)

    try:
        transactions=db.query(models.Transaction).filter(
            models.Transaction.created_at >= start_date,
            models.Transaction.created_at <= end_date
        ).all()
        
        total_amount = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0))
        .filter(
           
            models.Transaction.created_at >= start_date,
            models.Transaction.created_at <= end_date,
        )
        .scalar()
    )
        if not transactions:
            return HTTPException(status_code=200,detail="no transaction")
        return {
             year: year,
             month: month,
             "total_amount": total_amount,
            "transactions": transactions
            
        }
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    
#transactions per day
@router.get("/day/all",status_code=status.HTTP_200_OK)
async def get_day_transactions(
     date_: date = Query(..., alias="date", example="2025-01-20"),
    db: Session = Depends(get_db),

   ):
    
    start_datetime = datetime.combine(date_, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)
  
    try:
        transactions=db.query(models.Transaction).filter(
            models.Transaction.created_at >= start_datetime,
            models.Transaction.created_at <= end_datetime
        ).all()
        
        total_amount = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0))
        .filter(
           
            models.Transaction.created_at >= start_datetime,
            models.Transaction.created_at <= end_datetime,
        )
        .scalar()
    )
        if not transactions:
            return HTTPException(status_code=200,detail="no transaction")
        return {
            "date": date_,
             "total_amount": total_amount,
            "transactions": transactions
            
        }
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")