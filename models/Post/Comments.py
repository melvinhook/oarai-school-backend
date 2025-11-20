from sqlalchemy import Column,DateTime,Integer,String,ForeignKey,desc,func 
from sqlalchemy.orm import relationship
from ...database import base
class Comments(base):   
    __tablename__="comments"
    id=Column(Integer,primary_key=True,index=True,autoincrement=True) 
    content=Column(String,index=True)    
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    post_id=Column(Integer,ForeignKey("posts.id")) 
    user_id=Column(Integer,ForeignKey("users.id"))   
    users=relationship("User",back_populates="comments")   
    commentlikes=relationship("CommentLikes",back_populates="comment") 
    reply=relationship("Replies",back_populates="comment") 
    post=relationship("Posts",back_populates="comment",order_by=lambda: desc(Comments.created_at))
 
    
   



    