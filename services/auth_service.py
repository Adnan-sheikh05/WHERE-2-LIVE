import bcrypt
import os 
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def hash_password(password : str) :
    password_bytes = password.encode('utf-8')[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    print(plain_password , hashed_password)
    password_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))


def  create_access_token(data : dict , expires_minutes : int = 60) :
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= expires_minutes)
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode , SECRET_KEY , ALGORITHM)