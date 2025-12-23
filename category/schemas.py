from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name:str
    budget:int
    
class CategoryResponse(BaseModel):
        
    name: str

    model_config = ConfigDict(from_attributes=True)
