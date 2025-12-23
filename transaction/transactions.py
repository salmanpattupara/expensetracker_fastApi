from fastapi import APIRouter, Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
import transaction.models as models
import transaction.schemas as schemas
from database import get_db


#router
router=APIRouter(
    prefix="/transaction", tags=["transaction"]
)


#transaction 
@router.get("/")
async def transactions(db:Session=Depends(get_db)):
    try:
        result=db.query(models.Transaction).all()
        if not result:
            return HTTPException(status_code=200,detail="no transaction")
        return result
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    


@router.post("/")
async def new_transaction(transaction:schemas.TransactionCreate,db:Session=Depends(get_db)):
    try:
        db_txn=models.Transaction(**transaction.model_dump())
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
    
@router.get("/{id}")
async def get_transaction():
    try:
        pass
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
    
@router.put("/{id}")
async def edit_transaction():
    try:
        pass
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")
    
@router.delete("/{id}")
async def delete_transaction():
    try:
        pass
    except Exception as e:
        return HTTPException(status_code=500,detail=f"some error occured {e}")