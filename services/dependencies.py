from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError 
from sqlmodel import Session , select
from database import get_session
from models.user import User
from services.auth_service import SECRET_KEY , ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token : str = Depends(oauth2_scheme) , session : Session = Depends(get_session)) :
    try : 
        payload  = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError : 
        raise HTTPException(status_code=401 , detail="Invalid or Expired Token")
    user = session.exec(select(User).where(User.email == email)).first()
    if not user : 
        raise HTTPException(status_code=401 , detail="User not found")
    return user