from sqlalchemy import Column,Integer,ForeignKey,DateTime, UniqueConstraint,func
from sqlalchemy.orm import relationship
from ...database import base 
class CommentLikes(base): 
    __tablename__="commentlikes" 
    id=Column(Integer,autoincrement=True,primary_key=True,index=True) 
    comment_id=Column(Integer,ForeignKey("comments.id"))  
    user_id=Column(Integer,ForeignKey("users.id")) 
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    comment=relationship("Comments",back_populates="commentlikes") 
    user=relationship("User",back_populates="commentlikes")  


    