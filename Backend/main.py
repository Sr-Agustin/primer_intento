from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend import models, schemas, crud, database
from Backend.auth import create_access_token, verify_password

# Crear las tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# ==============================
# REGISTER
# ==============================
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Verificar email
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Verificar username
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username ya registrado")

    # Crear usuario
    new_user = crud.create_user(db, user)
    return new_user


# ==============================
# LOGIN
# ==============================
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=400, detail="Email incorrecto")

    # Verificar password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # Crear token
    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
        },
    }


# ==============================
# PROTECTED ROUTE EXAMPLE
# ==============================
from Backend.dependencies import get_current_user
@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": "Acceso permitido", "user": current_user.email}