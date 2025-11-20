from sqlalchemy import Column, ForeignKey, Integer, String   
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ...database import base 
class Employee(base): 
    __tablename__="employee" 
    id=Column(Integer,primary_key=True,autoincrement=True,index=True) 
    name=Column(String,index=True) 
    department=relationship("Department",back_populates="employee")  
    department_id = Column(Integer, ForeignKey("department.id"))