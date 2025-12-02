from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    db_user2 = crud.get_user_by_username(db, user.username)
    if db_user2:
        raise HTTPException(status_code=400, detail="Username ya registrado")

    new_user = crud.create_user(db, user)
    return new_user
