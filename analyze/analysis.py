from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
import category.models as models
import category.schemas as schemas
from database import get_db



router=APIRouter(
    prefix="/analytics", tags=["analytics"]
)


#total for each month
@router.get("/monthlytotal")
def get_monthlytotal():
    return {"status":200,"message":"not implimented"}

#category wise total for each month
@router.get("/categorytotal")
def get_categorytotal():
    return {"status":200,"message":"not implimented"}

