
import asyncio
from datetime import datetime, timedelta
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt, JWTError
from user.models import User
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import  get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CHANGE_ME_TO_A_SECURE_RANDOM_STRING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email: str, password: str,  db: Session,):
    user=db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user




async def  get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),):
   
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
       
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
   
    user = db.query(User).filter(User.id == user_id).first()
 
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return {"email":user.email,"id":user.id}