import os
import cloudinary
import cloudinary.uploader
import cloudinary.api  
from datetime import datetime 
from fastapi import APIRouter, File, Form,HTTPException,Depends, UploadFile 
from pydantic import BaseModel 
from passlib.context import CryptContext 
from sqlalchemy.orm import Session  
from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token , get_current_user
from ...dep import get_db 
from ...models.Users import models    
router=APIRouter()   
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")
class UserCreate(BaseModel): 
    username:str 
    email:str 
    password:str  
    borndate:str 
    firstname:str 
    lastname:str
class UserUpdate(BaseModel): 
    username:str|None=None 
    email:str|None=None  
    password:str|None=None 
class UserLogin(BaseModel): 
    username:str 
    password:str  
def hash(password:str)->str: 
    return pwd_context.hash(password) 
def verify(ppass:str,hpass:str)->bool: 
    return pwd_context.verify(ppass,hpass)  

@router.post("/users/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    borndate: str = Form(...),
    file: UploadFile = File(None),  # optional
    db: Session = Depends(get_db)
):
    try:
        hashed = hash(password)
        photo_url = None
        public_id = None
        # 🔹 Upload ke Cloudinary kalau ada file
        if file: 
            ext = os.path.splitext(file.filename)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{username}_{timestamp}{ext}"
            upload_result = cloudinary.uploader.upload(
                file.file,
                public_id=filename,
                folder="profile_photos",
                overwrite=True,
                resource_type="image"
            )
            photo_url = upload_result["secure_url"]
            public_id = upload_result["public_id"]
        new_user = models.User(
            username=username,
            email=email,
            password=hashed,
            first_name=firstname,
            last_name=lastname,
            borndate=borndate,
            profile_photos=photo_url,   # simpan URL di DB
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User created successfully ✅",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "profile_photo": photo_url,
                "public_id": public_id
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login/") 
def login(u:UserLogin,db:Session=Depends(get_db)): 
    similar=db.query(models.User).filter(models.User.username==u.username).first() 
    try: 
        if not similar: 
            raise HTTPException(status_code=404,detail="Invalid Username ORRR Pass") 
        if not verify(u.password,similar.password): 
            raise HTTPException(status_code=404,detail="Invalid Username ORRR Pass")  
        return {"Login Succesfully!"}
    except: 
        return {"Nope"}
@router.post("/jwtlogin/") 
def login(u:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)): 
    similar=db.query(models.User).filter(models.User.username==u.username).first() 
    try: 
        if not similar or not verify(u.password,similar.password): 
            raise HTTPException(status_code=404,detail="Invalid Username ORRR Pass") 
        access_token = create_access_token(data={"sub": u.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except: 
        raise HTTPException(status_code=404,detail="Not Found")   
@router.get("/users/get") 
def get_user_verify(current_user:str=Depends(get_current_user)): 
    return {"Username" : current_user} 
@router.get("/users/get_current_user")
def get_user_verify(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = db.query(models.User.id, models.User.first_name, models.User.last_name, models.User.profile_photos).filter(models.User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id":user.id,"firstname": user.first_name, "lastname": user.last_name, "profile_photo": user.profile_photos}
@router.get("/users/") 
def get_user(db:Session=Depends(get_db)): 
    return db.query(models.User).all() 
@router.put("/users/{user_id}") 
def update_user(user_id:str,u:UserUpdate,db:Session=Depends(get_db)): 
    get_user=db.query(models.User).filter(models.User.id==user_id).first() 
    if not get_user: 
        raise HTTPException(status_code=404,detail="User not real") 
    if u.username is not None: 
        get_user.username=u.username  
    if u.email is not None: 
        get_user.username=u.email  
    if u.password is not None: 
        get_user.username=u.password   
    db.commit() 
    db.refresh(get_user) 
    return {"They got them"} 
@router.delete("/users/{user_id}") 
def delete_user(user_id:str,u:UserUpdate,db:Session=Depends(get_db)): 
    get_user=db.query(models.User).filter(models.User.id==user_id).first() 
    if not get_user: 
        raise HTTPException(status_code=404,detail="User not real")  
    db.delete(get_user) 
    db.commit() 
    return {"user {get_user.username} no longer in this world"} 
@router.get("/users/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "profile_photo": user.profile_photo  # URL langsung dari Cloudinary
    } 
@router.get("/users/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email,
        "profile_photo": user.profile_photos  # URL langsung dari Cloudinary
    }