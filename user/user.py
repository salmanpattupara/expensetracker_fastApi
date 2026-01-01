from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from user.models import User
from user.schemas import UserCreate, UserResponse
from user.service import ACCESS_TOKEN_EXPIRE_MINUTES, hash_password,authenticate_user,create_access_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router=APIRouter(
    prefix="/user", tags=["user"]
)

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
  
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise   HTTPException(status_code=409,detail=f"user already exist")
    try:
        new_user = User(
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"something went wrong {e}")



@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email,"id":user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

@router.get("/me",status_code=status.HTTP_200_OK)
async def currentUser(user: user_dependency,response_model=UserResponse):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    return {"user":user}
        
