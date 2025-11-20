from pydantic import BaseModel 

class UserBase(BaseModel):
    name: str
class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostOut(PostBase):
    id: int
    owner: UserOut   # include user info
    class Config:
        orm_mode = True 
        
