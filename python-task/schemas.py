import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    name: str
    email: str
    
class UserCreate(_UserBase):
    password: str
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        
        
class User(_UserBase):
    id: int
    date_created: _dt.datetime
    
    class Config:
        orm_mode=True
        allow_population_by_field_name = True