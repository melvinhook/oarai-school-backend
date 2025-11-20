from sqlalchemy import Column, DateTime,String,Integer, func
from ...database import base
class PostTest(base): 
    __tablename__="post-test" 
    id=Column(Integer,autoincrement=True,index=True,primary_key=True)  
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    title=Column(String,index=True) 
    desc=Column(String,index=True)