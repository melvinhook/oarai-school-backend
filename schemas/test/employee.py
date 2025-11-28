from pydantic import BaseModel 
from typing import Optional  
from . import department 
class EmployeeBaseModel(BaseModel):
    name:str  
    department_id: int
class CreateEmployee(EmployeeBaseModel):
    pass 
class EmployeeOut(EmployeeBaseModel): 
    id:int 
    department:Optional[department.DepartmentOut]
    class config:  
        orm_mode=True
