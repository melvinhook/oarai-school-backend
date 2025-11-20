from fastapi import Depends,HTTPException 
from fastapi.security import OAuth2PasswordBearer 
from datetime import datetime,timedelta 
from jose import jwt,JWTError  
SECRET="akulupa" 
ALGORITHM="HS256" 
EXPIRED=30  
oauth2scheme=OAuth2PasswordBearer(tokenUrl="jwtlogin")
def get_token(data:dict,expire_delta:timedelta|None=None): 
    to_encode=data.copy() 
    expire=datetime.utcnow()+(expire_delta or timedelta(minutes=EXPIRED)) 
    to_encode.update({"exp":expire}) 
    jwtencode=jwt.encode(expire,SECRET,algorithm=ALGORITHM) 
    return jwtencode 
def verify_user(token:str): 
    try:  
        verify=jwt.decode(token,SECRET,algorithms=[ALGORITHM]) 
        return verify
    except JWTError:  
        return None 
def get_user_token(token:str=Depends(oauth2scheme)): 
    try: 
        verify=jwt.decode(token,SECRET,algorithms=[ALGORITHM])  
        username:str=verify.get("sub") 
        if username is None: 
            raise HTTPException(status_code=401,detail="invalid token") 
    except JWTError: 
        raise HTTPException(status_code=401,detail="invalid token") 