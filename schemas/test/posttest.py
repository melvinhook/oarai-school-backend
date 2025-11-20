from pydantic import BaseModel 
from typing import List, Optional  
from .department import DepartmentOut
class PostTestBaseModel(BaseModel):
    title:str
    desc:str
class CreatePostTest(PostTestBaseModel):
    pass 
class PostTestOut(PostTestBaseModel): 
    title:str 
    desc:str
    class config:  
        orm_mode=True 
class PostResponse(BaseModel):
    posts: List[PostTestOut]
    new_ids: List[PostTestOut]
