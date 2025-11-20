from pydantic import BaseModel
class UserBase(BaseModel): 
    username:str 
    first_name:str 
    last_name:str 
    email:str 
    password:str 
class UserCreate(UserBase): 
    pass 
class UserOut(UserBase):  
    id:int
    username:str 
    first_name:str 
    last_name:str 
    email:str  
    profile_photos:str