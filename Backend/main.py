from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from Backend import models, schemas, crud, database
from Backend.auth import create_access_token, verify_password
from Backend.routers import appointments

app = FastAPI()  #  Crear app primero

# Registrar routers
app.include_router(appointments.router)

# Crear las tablas
models.Base.metadata.create_all(bind=database.engine)


# ==============================
# REGISTER
# ==============================
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Verificar email
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Email incorrecto")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
    }



# ==============================
# PROTECTED ROUTE EXAMPLE
# ==============================
from Backend.dependencies import get_current_user

@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": "Acceso permitido", "user": current_user.email}