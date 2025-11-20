from fastapi import FastAPI, Depends,  APIRouter, Query, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session  
from ...models.Test import department as departmentModel , employee as employeeModel , posttest as posttestmodel
from ...schemas.test import scheme  
from ...schemas.test import employee 
from ...schemas.test import department 
from ...schemas.test import posttest
from ...dep import get_db  
router=APIRouter(prefix="/test")   
current_ids = set()  
def update_id_fit(db: Session, all_posts):
    global current_ids
    
    # ambil semua id dari hasil query
    new_ids = [p.id for p in all_posts]
    
    # cari id baru yang belum ada
    new_items_ids = set(new_ids) - current_ids
    
    if new_items_ids:
        print("🆕 ID baru ditemukan:", new_items_ids)
        # update current_ids
        current_ids.update(new_items_ids)
        # ambil data post yang id-nya termasuk baru
        new_items = [p for p in all_posts if p.id in new_items_ids]
        return new_items
    else:
        print("Tidak ada ID baru")
        return []  # biar selalu aman

def get_posts_with_user(db: Session):
    posts = db.query(department.Department).all()
    return posts 
@router.get("/posts", response_model=list[scheme.PostOut])
def read_posts(db: Session = Depends(get_db)):
    return get_posts_with_user(db)    
@router.post("/employee",response_model=employee.EmployeeOut) 
def post_employee(payload:employee.CreateEmployee,db:Session=Depends(get_db)):   
    new_employee=employeeModel.Employee(
        name=payload.name ,
        department_id=payload.department_id
    ) 
    db.add(new_employee) 
    db.commit() 
    db.refresh(new_employee) 
    return new_employee 
@router.post("/department",response_model=department.DepartmentOut) 
def post_department(payload:department.DepartmentCreate,db:Session=Depends(get_db)): 
    new_department=departmentModel.Department(
        name=payload.name
    ) 
    db.add(new_department) 
    db.commit() 
    db.refresh(new_department) 
    return new_department 
@router.get("/employee",response_model=list[employee.EmployeeOut]) 
def get_employee(db:Session=Depends(get_db)): 
    get_emp=db.query(employeeModel.Employee).all() 
    return get_emp 
@router.get("/employee/{id}",response_model=employee.EmployeeOut) 
def get_employee(id:int,db:Session=Depends(get_db)): 
    get_emp=db.query(employeeModel.Employee).filter(employeeModel.Employee.id==id).first() 
    return get_emp 
@router.get("/employee/search/{src}", response_model=list[employee.EmployeeOut])
def search_employee(src:str,db: Session = Depends(get_db)):
    # Perform case-insensitive search
    employees = (
        db.query(employeeModel.Employee)
        .filter(func.lower(employeeModel.Employee.name).like(func.lower(f"{src}%")))
        .all()
    )
    return employees   
@router.get("/employee/search-department/{dprt}", response_model=list[employee.EmployeeOut])
def search_by_department(
    dprt: str,
    db: Session = Depends(get_db)
):
    dprt = dprt.lower()
    departments = (
        db.query(departmentModel.Department)
        .filter(func.lower(departmentModel.Department.name).like(f"{dprt}%"))
        .all()
    )
    if not departments:
        raise HTTPException(status_code=404, detail="No departments found")
    department_ids = [d.id for d in departments]
    employees = (
        db.query(employeeModel.Employee)
        .filter(employeeModel.Employee.department_id.in_(department_ids))
        .all()
    )
    return employees 

@router.get("/department",response_model=list[department.DepartmentOut]) 
def get_dep(db:Session=Depends(get_db)): 
    get_dep=db.query(departmentModel.Department).all()
    return get_dep    

@router.get("/posttest", response_model=posttest.PostResponse)
def get_posttest(db: Session = Depends(get_db)):
    posts = db.query(posttestmodel.PostTest)\
              .order_by(posttestmodel.PostTest.created_at.desc())\
              .all()
    new_posts = update_id_fit(db, posts)
    return {
        "posts": posts,
        "new_ids": new_posts  # kirim data post baru, bukan cuma id
    }

@router.post("/posttest",response_model=posttest.PostTestOut) 
def create_posttest(payload:posttest.CreatePostTest,db:Session=Depends(get_db)): 
    create_posttest=posttestmodel.PostTest(
        title=payload.title, 
        desc=payload.desc
    )   
    db.add(create_posttest) 
    db.commit() 
    db.refresh(create_posttest) 
    return create_posttest 

    
    
    





