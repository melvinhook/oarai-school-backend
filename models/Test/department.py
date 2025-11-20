from sqlalchemy import Column, Integer, String   
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ...database import base 
class Department(base): 
    __tablename__="department" 
    id=Column(Integer,primary_key=True,autoincrement=True,index=True) 
    name=Column(String,index=True) 
    employee=relationship("Employee", back_populates="department")  
    

    