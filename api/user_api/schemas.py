from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
#password not returning
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_config = {"from_attributes": True}