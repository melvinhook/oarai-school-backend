from pydantic import BaseModel  
class DepartmentBaseModel(BaseModel): 
    name:str 
class DepartmentCreate(DepartmentBaseModel): 
    pass 
class DepartmentOut(DepartmentBaseModel): 
    id:int 
    class config: 
        orm_mode=True 
