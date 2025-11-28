from fastapi import Depends , HTTPException, Header
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
    # Coba ambil token dari header standar: Authorization: Bearer <token>
    auth_header: str = Depends(oauth2_scheme), 
    # Coba ambil token dari header kustom: X-Custom-Auth: Bearer <token>
    x_custom_auth: str | None = Header(None, alias="X-Custom-Auth") 
): 
    print("=== get_current_user CALLED ===")
    
    # PENTING: Tentukan token mana yang akan digunakan
    # Prioritaskan header standar, jika tidak ada, gunakan header kustom
    token = auth_header 
    print("Raw token (from header):", token)
    # Jika token standar tidak ada, dan token kustom ada, gunakan token kustom
    # Catatan: Header kustom biasanya tidak otomatis di-handle oleh OAuth2PasswordBearer
    if not token and x_custom_auth:
        # Asumsikan formatnya juga "Bearer <token>"
        if x_custom_auth.startswith("Bearer "):
            token = x_custom_auth.replace("Bearer ", "")
        else:
            token = x_custom_auth # Jika Anda kirim token mentah tanpa "Bearer"
    
    # --- Proses Verifikasi Token ---
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
        
    try:
        # Jika token masih dalam format 'Bearer <token>', kita harus menghilangkannya.
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        print("Decoded payload:", payload)
        username: str = payload.get("sub")
        print("Extracted username:", username)
        if username is None: 
            print("❌ No username inside token")
            raise HTTPException(status_code=401, detail="Invalid token payload") 
        print("=== TOKEN VALID ===")
        return username
    except JWTError: 
        print("❌ JWT ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

