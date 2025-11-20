from datetime import datetime
from pydantic import BaseModel 
from typing import List, Optional  
from ..User.scheme import UserOut  
class PostLikesBase(BaseModel): 
    post_id:int 
    user_id:int 
class PostLikesCreate(PostLikesBase): 
    pass 
class PostLikesOut(PostLikesBase): 
    post_id:int   
    user_id:int 
    user: Optional[UserOut] = None
    class Config: 
        orm_mode=True  
class LikeResponse(BaseModel):
    liked: bool
    message: str
class CommentLikesBase(BaseModel): 
    comment_id:int  
    user_id:int
class CommentLikesCreate(CommentLikesBase): 
    pass 
class CommentLikesOut(CommentLikesBase): 
    comment_id:int  
    user: Optional[UserOut] = None
    class Config: 
        orm_mode=True 
class ReplyLikesBase(BaseModel): 
    reply_id:int  
    user_id:int
class ReplyLikesCreate(ReplyLikesBase): 
    pass 
class ReplyLikesOut(ReplyLikesBase): 
    reply_id:int  
    user: Optional[UserOut] = None
    class Config: 
        orm_mode=True   
class ReplyBase(BaseModel): 
    content:str 
    user_id:int  
    comment_id:int 
class ReplyCreate(ReplyBase): 
    pass 
class ReplyOut(ReplyBase):  
    id:int
    content:str 
    users:Optional[UserOut]    
    replylikes: Optional[List[ReplyLikesOut]] = []  
    class Config: 
        orm_mode=True  
class CommentBase(BaseModel): 
    content:str 
    user_id:int  
    post_id:int
class CommentCreate(CommentBase): 
    pass 
class CommentOut(CommentBase):  
    id:int
    content:str    
    created_at:datetime 
    users:Optional[UserOut]   
    reply:Optional[List[ReplyOut]] = [] 
    commentlikes: Optional[List[CommentLikesOut]] = []   
    class Config: 
        orm_mode:True   

class CommentResponse(BaseModel):
    comment: List[CommentOut]
    new_ids: List[CommentOut]


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    user_id: Optional[int] = None
    cover: Optional[str] = None

class PostCreate(PostBase): 
    pass  
class PostOut(PostBase):  
    id:int
    title:str 
    content:str  
    slug:str 
    created_at:datetime  
    postlikes: Optional[List[PostLikesOut]] = []      
    comment: Optional[List[CommentOut]] = []   
    users: Optional[UserOut] = None
    class Config: 
        orm_mode=True  

class PostWithCustomCommentRange(BaseModel): 
    posts:list[PostOut] 
    new_ids:list[CommentOut] 









    


      



