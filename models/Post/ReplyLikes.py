from sqlalchemy import Column,Integer,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship
from ...database import base 
class ReplyLikes(base): 
    __tablename__="replylikes" 
    id=Column(Integer,autoincrement=True,primary_key=True,index=True) 
    reply_id=Column(Integer,ForeignKey("replies.id"))  
    user_id=Column(Integer,ForeignKey("users.id")) 
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    reply=relationship("Replies",back_populates="replylikes") 
    user=relationship("User",back_populates="replylikes") 

    