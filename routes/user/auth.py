from fastapi import HTTPException, Header, Cookie
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
# Secret key (generate your own with: openssl rand -hex 32)
SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwtlogin")
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt 
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains user_id / username etc.
    except JWTError:
        return None   
def get_current_user(
    jwt_cookie: str | None = Cookie(None, alias="jwt"),
    auth_header: str | None = Header(None, alias="Authorization")
):
    print("=== get_current_user CALLED ===")

    # Ambil token dari cookie dulu
    token = jwt_cookie

    # Jika tidak ada cookie, coba dari Authorization header
    if not token and auth_header:
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
        else:
            token = auth_header

    print("Raw token:", token)

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)
        username = payload.get("sub")
        print("Extracted username:", username)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        print("=== TOKEN VALID ===")
        return username
    except JWTError:
        print("❌ JWT ERROR")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

