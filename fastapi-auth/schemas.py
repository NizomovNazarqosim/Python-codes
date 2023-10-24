from pydantic import BaseModel
from uuid import UUID

#---------- user schemas
class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    
    class Config:
        from_attributes = True
        
class UserId(BaseModel):
    id: UUID
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email:str
    password: str
    
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    token:str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name:str or None
    email:str or None
    password:str or None
    
    class Config:
        from_attributes = True
    
        

#---------- post schemas
class PostCreate(BaseModel):
    title:str
    text:str
    user_id:str
    
    class Config:
        from_attributes = True
        
