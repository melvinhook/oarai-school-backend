from sqlalchemy import Column,Integer,ForeignKey,DateTime, UniqueConstraint,func
from sqlalchemy.orm import relationship
from ...database import base 
class PostLikes(base): 
    __tablename__="postlikes" 
    id=Column(Integer,autoincrement=True,primary_key=True,index=True) 
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE")) 
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))  
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    posts=relationship("Posts",back_populates="postlikes") 
    user=relationship("User",back_populates="postlikes") 
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),
    )
    