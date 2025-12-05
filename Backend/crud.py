from sqlalchemy.orm import Session
from Backend import models, schemas
from .auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pass = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ======================
# APPOINTMENTS
# ======================

def create_appointment(db: Session, user_id: int, appointment: schemas.AppointmentCreate):
    new_appointment = models.Appointment(
        user_id=user_id,
        date=appointment.date,
        time=appointment.time,
        status=appointment.status
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

def get_user_appointments(db: Session, user_id: int):
    return db.query(models.Appointment).filter(models.Appointment.user_id == user_id).all()

def delete_appointment(db: Session, appointment_id: int, user_id: int):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == user_id
    ).first()

    if appointment:
        db.delete(appointment)
        db.commit()
        return True

    return False
