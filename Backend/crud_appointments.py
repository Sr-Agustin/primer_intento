from sqlalchemy.orm import Session
from Backend import models, schemas

# Crear un turno
def create_appointment(db: Session, user_id: int, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(
        user_id=user_id,
        date=appointment.date,
        time=appointment.time,
        status=appointment.status
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Obtener todos los turnos
def get_all_appointments(db: Session):
    return db.query(models.Appointment).all()


# Obtener los turnos de un usuario
def get_user_appointments(db: Session, user_id: int):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.user_id == user_id)
        .all()
    )


# Cancelar o cambiar estado de un turno
def update_appointment_status(db: Session, appointment_id: int, status: str):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment:
        appointment.status = status
        db.commit()
        db.refresh(appointment)
    return appointment


# Eliminar turno
def delete_appointment(db: Session, appointment_id: int):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
    return appointment
