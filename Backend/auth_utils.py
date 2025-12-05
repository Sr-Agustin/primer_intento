from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend import crud, models
from Backend.config import settings   # <── AGREGADO

# URL donde Swagger pide el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.SECRET_KEY      # <── USAMOS LA MISMA QUE auth.py
ALGORITHM = settings.ALGORITHM        # <── IGUAL
                                      

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud.get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
