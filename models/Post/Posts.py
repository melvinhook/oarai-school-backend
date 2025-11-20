from sqlalchemy import Column, Date,Integer,String,ForeignKey,DateTime, desc,func    
from sqlalchemy.orm import relationship  
from .Comments import Comments
from ...database import base 
class Posts(base): 
    __tablename__="posts" 
    id=Column(Integer,primary_key=True,index=True,autoincrement=True) 
    title=Column(String,index=True) 
    content=Column(String,index=True)  
    slug=Column(String,index=True)   
    cover=Column(String,index=True) 
    user_id=Column(Integer,ForeignKey("users.id"))  
    created_at = Column(Date, server_default=func.current_date())
    updated_at=Column(DateTime(timezone=True), onupdate=func.now())  
    users=relationship("User",back_populates="posts")    
    postlikes=relationship("PostLikes",back_populates="posts")   
    comment=relationship("Comments",back_populates="post",order_by=desc(Comments.created_at)) 

    """ 
      comment = relationship(
        "Comments",
        back_populates="post",
        order_by=desc(Comments.created_at)
    )
    """




 



    

    
