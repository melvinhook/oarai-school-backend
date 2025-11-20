from sqlalchemy import Column,Integer,String,Date,ForeignKey
from sqlalchemy.orm import relationship
from ...database import base 
class User(base): 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True) 
    username = Column(String, index=True)  
    first_name = Column(String, index=True) 
    last_name = Column(String, index=True)
    email = Column(String, index=True) 
    password = Column(String, index=True)    
    borndate = Column(Date, nullable=True)  
    profile_photos = Column(String, index=True) 
    posts=relationship("Posts",back_populates="users")   
    comments=relationship("Comments",back_populates="users")   
    replies=relationship("Replies",back_populates="users")   
    postlikes=relationship("PostLikes",back_populates="user")   
    commentlikes=relationship("CommentLikes",back_populates="user")  
    replylikes=relationship("ReplyLikes",back_populates="user")
  





    
 
    




    


