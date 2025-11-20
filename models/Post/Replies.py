from sqlalchemy import Integer,Column,String,ForeignKey,DateTime,func 
from sqlalchemy.orm import relationship
from ...database import base
class Replies(base): 
    __tablename__="replies" 
    id=Column(Integer,index=True,primary_key=True,autoincrement=True) 
    content=Column(String,index=True)  
    user_id=Column(Integer,ForeignKey("users.id")) 
    comment_id=Column(Integer,ForeignKey("comments.id"))  
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    users=relationship("User",back_populates="replies")  
    replylikes=relationship("ReplyLikes",back_populates="reply") 
    comment=relationship("Comments",back_populates="reply") 