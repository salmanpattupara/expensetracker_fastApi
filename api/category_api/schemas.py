from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name:str
 
    
class CategoryResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)
    
    
    
    
class User_categoryBase(BaseModel):
   
    name:str
    budget:int  
    model_config = ConfigDict(from_attributes=True)
    
    
class User_categoryResponse(BaseModel):
    id:int
    category:CategoryResponse
    budget:int
    model_config = ConfigDict(from_attributes=True)
